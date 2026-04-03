# 🤖 MIT EECS 6.01 - 实验代码库

🌟 **这是 MIT-EECS-6.01 部分实验代码，上机效果良好！**

✨ 本项目基于 Python 2.6 开发。部分实验依赖于课程官方提供的 lib601 库，请确保将其放置在 Python 环境变量或项目根目录中
```mermaid
graph TD
    A[传感器读取 (Sensors)] --> B{状态机判断 (State Machine)}
    B -->|前方无障碍| C[比例控制推进 (P-Control)]
    B -->|检测到障碍| D[壁面跟随算法 (Wall Following)]
    B -->|到达目标| E[终止状态 (Halt)]
    C --> F[电机驱动指令 (Actuators)]
    D --> F
    F --> A
```
