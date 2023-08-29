# **ContentAI Ad Conditioning** 
Repo Breakdown:
- analysis: Contains statistical analysis explorations into black screens and places. 
- gif_visualizations: Contains utility code for generating gifs of ad candidates (or expert labels) for easier viewing at scale.
- extractors: Contains all code related to individual extractors, combination logic, and generating results. This is folder is the focal point of the repo and it is explained in great detail below.

## AdReady

System of individual extractors and scene analysis tools for recommending scene boundaries that may be good ad placement candidates.

Implemented:
 - [X] Black Screen Strict
 - [X] Black Screen Lenient
 - [X] Silence
 - [X] Shot Transition
 - [X] Places
 - [ ] People
 - [ ] Speech
 - [ ] Audio
 - [ ] Action

## For running on the ContentAI cloud platform

While connected to the VPN you can find in-depth documentation on the setup for ContentAI as well as usage on all the commands for utilizing the tooling most effectively at this page https://contentai.io/docs/cli

The ContentAI command line tool provides functionality for running any content stored in S3. You can run pieces of content individually or create a batch script to run muliple pieces of content at once. More info on creating a batch script can be found at the link above.

Within the ContentAI environment the extractors have the following names:

- `ad_conditioning_black_screen_strict`
  - Identifies near fully black frames in content.
- `ad_conditioning_black_screen_lenient`
  - Identifies darker, not fully black, frames in content.
- `ad_conditioning_silence`
  - Identifies spans of silence in content.
- `ad_conditioning_places`
  - Identifies place changes in content, on both a frame-by-frame basis and a window-based approach which compares two equal windows of time prior to and after a specific time and provides a score to denote how 'different' those windows or frames are from eachother.
- `ad_conditioning_shot_transition`
  - Identifies shot changes in content, which can be defined as any time the camera angle changes.
- `ad_conditioning_markers`
  - Utility for converting ad markers json into a format that the scene_breaker extractor understands
- `ad_conditioning_scene_breaker`
  - Combines all the signal from the extractors listed above to generate AI ad candidates and produce metrics comparing the AI candidates to the actual expert labeled ad breaks.

### Example usage

The following would be an example script for running the `ad_conditioning_silence` extractor on a specific piece of content within S3:
```
contentai run 's3://PATH’ -w 'digraph { ad_conditioning_silence }'
```
The following would be an example script for running the `ad_conditioning_black_screen_strict` extractor on a specific piece of content within S3:
```
contentai run 's3://PATH’ -w 'digraph { ad_conditioning_black_screen_strict }'
```
The above command structure also works for `ad_conditioning_black_screen_lenient` and `shot_transition`. 

The `ad_conditioning_places` and `ad_conditioning_scene_breaker` extractors are slightly different. Running `ad_conditioning_places` has parameters, and could look something like this, depending on what arguments you'd like to change:
```
contentai run 's3://PATH' -d '{ "ad_conditioning_places_args":["--save_png"] }' -w 'digraph { ad_conditioning_places }'
```

See sections below for further details on the parameters.

Lastly, once a piece of content has been run on all the extractors above (black_screen_strict, black_screen_lenient, silence, places, and shot_transition) you can then pass this command to run the scene_breaker, which will search an inventory of ad markers to check if the markers for this specific piece of content exists. It will then consolidate all the signal from the previous extractors to produce the AI ad candidates. This extractor will produce ad candidates, metrics for comparing to expert ad markers, and visualizations of all parts of the system. This command will look like this:

Note: This will fail if the ad markers for this piece of content don't exist, it will also fail if any of the prior extractors have not yet been run on this piece of content.

```
contentai run 's3://PATH’ -w ‘digraph { ad_conditioning_markers -> ad_conditioning_scene_breaker }’
```

## Installation for running locally

### Basic utilities
For a Mac developer on a machine without basic utilities, first get *wget*:
```
brew install wget
```

### Virtual environment
Then setup a virtual environment, *e.g.* via Conda .  Here is how to install that:
```
cd ~
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh -O ~/miniconda.sh
bash ~/miniconda.sh -p $HOME/miniconda
```
Type "yes" and "yes" to finish the Conda installation. Launch a new shell.
Then launch a virtual environment with Python 3.10:
```
conda create --name ad_ready python=3.10
conda activate ad_ready
```

### Python dependencies
First navigate into the extractors folder within your local version of the repo and install the necessary libraries: 
```
cd contentai-ad-conditioning/extractors
python -m pip install -r ./requirements.txt
```
Note: The 'boto3' and 'contentaiextractor' libraries aren't required for running locally so you can remove those if either is causing issues while installing.

### Running locally

First navigate to the extractors folder
```
cd contentai-ad-conditioning/extractors
```
For running any of the following: black_screen_strict, black_screen_lenient, silence, shot_transition, places, end_to_end the first five in that list are the individual extractors and are self explanatory. As for end_to_end, it will take a piece of content and run it through the entire system and then pass it to scene_breaker and produce ad candidates (using the end_to_end mode will most likely be the most useful command) but they will all share the same form, here is a few examples:
```
python main.py --video_path path.mp4 --detect_mode end_to_end
```
```
python main.py --video_path path.mp4 --detect_mode black_screen_strict
```

If you already have the csv outputs from black_screen_strict, black_screen_lenient, silence, shot_transition, and places. You can utilize the scene_breaker extractor alone which will take in those csv's and then produce ad candidates, that command would look something like this:
```
python main.py --detect_mode scene_breaker --black_screen_strict strict.csv --black_screen_lenient lenient.csv --silence silence.csv --shot_transition shot_transition.csv --place_transition place_transitions.csv
```
Note: The command listed directly above will run with or without ad markers being present. If you do have the ad markers for the content and it's in the correct format that scene_breaker understands you can pass in this additional command line argument with the command above `--ad_markers markers.csv`. It is required that the markers csv be stored in the current directory with the name `markers.csv`.

Below is additional information on running the deep feature extractor (referred to as places extractor above) from source which allows you to access more of the options and tweak them if you'd like to play around with that. There is also additional information on the scene breaker source code which lists out the various options that are availble to tweak if you'd like to run that from source. It also has explanations for what all the options represent if you'd like to look into that more.

## Running places extractor from source

For GPU production deployment, it is recommended to go out of the way to install PyTorch 2.0, since it can be 2x faster.  See [here](https://pytorch.org/get-started/pytorch-2.0/#faqs).

### Download pre-trained weights for deep learning models
Get the weights for a ResNet-50 model trained on [Places365 data](http://places2.csail.mit.edu/index.html):
```
cd contentai-ad-conditioning/extractors
python download_models.py
```

Extract deep place features from a video:
```
python deep_feature_extractor.py --video_path path/to/some.mp4
```
To save an output .csv with place transition scores, set `--save_csv` to `True`.  
To save an output graph visualization, set `--save_png` to `True`.  
To use an available GPU, set `--use_gpu` to `True`.  
To process one out of every 30 frames, set `--skip_n_frames` to `30`.  
To consider +-10 seconds in place transitions, set `--n_window_seconds` to `10`.  

### Running scene breaker from source
After running all narrow classifiers, their .csv outputs are chained together, and logically considered, in one "central brain" recommendation engine, which we call the "scene breaker" (`scene_breaker.py`).

Here is a command with all available flags for running that:

```
python scene_breaker.py --content_url "unique_identifier_string"
                        --black_screen_strict "black_screen_strict.csv" 
                        --black_screen_lenient "black_screen_lenient.csv"
                        --silence "silence.csv" 
                        --shot_transition "shot_transition.csv"
                        --place_transition "deep_place_transitions.csv"
                        --scene_break_labels "N/A"
                        --ad_markers "ad_markers.csv"
                        --save_graph_of_data_visualization "True"
                        --save_csv_of_top_scene_breaks
                        --n_scene_breaks_per_minute 0.5       
                        --minimum_seconds_between_scene_breaks 75  
                        --weight_of_black_screen_strict 2.5
                        --weight_of_black_screen_lenient 0.10     
                        --weight_of_silence 0.01      
                        --weight_of_shot_transition 0.05  
                        --weight_of_frame_to_frame_place_transition 0.30      
                        --weight_of_window_to_window_place_transition 0.15
                        
```
The first flag, `--content_url` can include an actual URL of the video, which has been used in cloud processing for further automated analytics. However, in any case, when running locally, any "unique_identifier_string" will be useful as a means of identifying outputs from this run.

Above, each of the .csv files are outputs the respective system, *e.g.* `black_screen_strict.csv` comes from the strict-version of the black screen detector.  

Previously, we manually curated scene break labels for visual and statistical analysis, which is what the flag `scene_break_labels` is for, but by default entering "N/A" or leaving that blank will be fine.  

The `ad_markers` flag is for adding a .csv file of corresponding real-world ad markers for each video.  If these are not available, entering "N/A" will be fine.  

The flags `save_graph_of_data_visualization` and `save_csv_of_top_scene_breaks` are there to potentially avoid saving output descriptive files (namely, a data visualization as a .png, and recommended scene breaks as a .csv output), but by default these will be true.

Two flags not identified above, because they do not lead to better performance and are not required (yet), are `--silence_required` and `--shot_transition_required`.  In both cases, if they are set, then they force the scene break candidates to be silent and/or a shot transition, respectively.  The shot transition enforcement functionality, in particular, is not yet mature and still a work-in-progress.

The remainder of the flags are numerical parameters of the scene break algorithm (in its current, imature, prototype state, which should be subject to significant improvements and changes in near future).

First of all, two key parameters that determine the quantity of ad candidate recommendations:

  - `n_scene_breaks_per_minute` = The maximum number of scene breaks per minute, across the entire video. This technically will determine N total scene breaks recommended.  However, it is possible that there are not this many good ad candidates, sufficiently spaced out.
  - `minimum_seconds_between_scene_breaks` = The parameter that technically defines the minimum spacing between scene break candidates. Technically, once the scene break algorithm identifies the top-ranked candidate, it prevents any additional candidates within this many seconds around the first recommendeded ad candidate.  Then, it finds the next top-ranked candidate in the remaining qualified blocks of time.

And then, for the current system, which is not considered to be the most effective, but was a first-pass prototype, weights of importance may be set. Technically, these weights have never been optimized to date, and so the default weights shown below were simply hand-tuned by quick reference.  

  - `--weight_of_black_screen_strict 2.5` = The weight of the strict black screen detector, which is most reliable today.  These are always top candidates.
  - `--weight_of_black_screen_lenient 0.10` = The weight of the less trustworthy, more noisy, but still useful "lenient" black screen detector.    
  - `--weight_of_silence 0.01` = The weight of silences (practically meaningless in current system).
  - `--weight_of_shot_transition 0.05` = The weight of shot transitions, which can be useful to try to ensure scene breaks are not disruptive in the middle of a scene action sequence.  This will be further exploited in future planned development.
  - `--weight_of_frame_to_frame_place_transition 0.30` = The weight of the "frame-to-frame" place transition score.  This is a system that naively measures the deep place embedding transitions, from one frame to the next, and computes the Euclidian distances, and then normalizes them by video.
  - `--weight_of_window_to_window_place_transition 0.15` = Same as above, except for the "window-to-window" place transition score, this considers instead of just one frame to the next, entire windows of videos (e.g. 30 seconds) into the past, versus windows into the future.  This can be useful to help prevent recommending scene breaks, during the middle of back-and-forth changes.  This is still not yet mature and needs to be further developed to be reliable.

It is likely that some alternative weighting sheme would deliver significantly better performance, in various cases.  More generally, it is likely that a neural network that learns to pinpoint positions of real world ad markers (i.e. from our large real ad marker dataset) would dramatically out-perform the existing system (and many other options).  Finally, to assist with explainability and modularity of the AI, it will still be possible to query the "attention" of such a neural network: we will be able to inform ad candidate reviewers downstream what types of intelligence (e.g. place change, person change, black screen, ...) was *most* responsible for each scene break score.

Lastly, it's worth stating something that may not be obvious: our system technically produces scene break scores for *every moment in the video* (technically, at least 3 scene break scores per second).  This dense, raw information could be extracted from the scene_breaker.py (although it is not currently output in full), if it could be useful downstream in a UI for ad candidate reviewers.

Also, for future development, it is fully known that several additional narrow AI classifiers will significantly improve performance and reliability.  These include, but are not limited to: 

  - *Persons* = Neural networks trained to (I) identify pixels of unique people in the [Cast in Movies dataset](https://arxiv.org/pdf/1806.03084.pdf), (II) extract deep features of the people based on the [People in Photo Albums dataset](https://arxiv.org/pdf/1501.05703.pdf)
  - *Audio* = Neural networks trained to (I) separate speech and background sound trained on the [AV Active Speaker dataset](https://arxiv.org/pdf/1808.00606.pdf), (II) generatively represent the audio signal through deep features, e.g. [wav2vec2](https://ai.facebook.com/blog/wav2vec-20-learning-the-structure-of-speech-from-raw-audio/)
  - *Actions* = Neural networks trained to classify the actions of people (e.g. from [AV Actions dataset](https://github.com/cvdfoundation/ava-dataset))

#### Acknowledgements
Techniques inspired by [Rao et al. (CVPR 2020)](https://arxiv.org/pdf/2004.02678.pdf). ResNet-50 place features from [MovieNet](https://github.com/movienet/movienet-tools).  
Developed with 🖤 at Warner.