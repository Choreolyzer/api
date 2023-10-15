#!/bin/bash
source ~/.bashrc

echo "Running yolox"
cd /home/rayb/Documents/yolox/
rm export/*
source venv/bin/activate
export PYTHONPATH="{PYTHONPATH}:/home/rayb/Documents/yolox/" && python tools/demo.py video -n yolox-m -c yolox_m.pth --path ../choreolyzer-api/assets/video.mp4 --conf 0.75 --nms 0.45 --tsize 640 --save_result --device gpu
deactivate

echo "Moving files over"
rm ../motrv2/data/Dataset/mot/DanceTrack/test/blackpink/img1/*
rm ../motrv2/data/Dataset/mot/deb_db_motrv2.json
mv export/*.jpg ../motrv2/data/Dataset/mot/DanceTrack/test/blackpink/img1/
mv export/data.json ../motrv2/data/Dataset/mot/det_db_motrv2.json

echo "Running motrv2"
cd /home/rayb/Documents/motrv2/
# conda activate motrv2
conda run -n motrv2 ./tools/simple_inference.sh ./motrv2_dancetrack.pth

echo "Running visualizer"
cd tracker
conda run -n motrv2 python vis.py
# conda deactivate

echo "Moving bp.txt, out.webm"
rm ../../choreolyzer-api/assets/out.webm
rm ../../choreolyzer-api/assets/out.txt
mv out.webm ../../choreolyzer-api/assets/out.webm
mv blackpink.txt ../../choreolyzer-api/assets/out.txt

cd ../../choreolyzer
