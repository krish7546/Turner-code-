#!/bin/bash

# On error exit
set -e

contentai deploy -f .github/ad_conditioning_black_screen_strict.yml -v
contentai deploy -f .github/ad_conditioning_black_screen_lenient.yml -v
contentai deploy -f .github/ad_conditioning_silence.yml -v
contentai deploy -f .github/ad_conditioning_shot_transition.yml -v
cd ./src
contentai deploy -f ../.github/ad_conditioning_places.yml -v
contentai deploy -f ../.github/ad_conditioning_markers.yml -v
contentai deploy -f ../.github/ad_conditioning_scene_breaker.yml -v
