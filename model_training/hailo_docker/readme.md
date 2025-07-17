# Convert PyTorch Models to Hailo Compatible Format for RPI5

## Requirements
- hailo ai sw suite (tar gz file)
- hailo ai sw suite (docker sh file)
- trained model (exported to ONNX format)

## Process:
0. File Placement:
- Place the tar gz file and the sh file under the same directory (with readme)
- Files needed:
    - ```hailo_ai_sw_suite_docker_run.sh```
    - ```hailo_ai_sw_suite_2025-04.tar.gz```

1. Activate/Create Docker Environment
- For the first time
```bash
./hailo_ai_sw_suite_docker_run.sh
```
- or
```bash
./hailo_ai_sw_suite_docker_run.sh --resume
```

- Then place the onnx model under ```shared_with_docker``` directory

2. Parse Model
```bash
hailo parser onnx /local/shared_with_docker/best.onnx 
```

3. Optimize Model
```bash
hailo optimize --hw-arch hailo8l /local/workspace/best.har --use-random-calib-set
```

4. Compile Model
```bash
hailo compiler --hw-arch hailo8l /local/workspace/best_optimized.har 
```

- During the process, the engine will ask you about some configurations/settings, simply respond 'y' as yes to all questions.

- Then ```best.hef``` will be generated. Copy it onto Raspberry Pi to proceed.