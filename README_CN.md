# EPD-nRF5

基于 Nordic nRF5 系列 MCU 的墨水屏固件项目。支持中国农历、节气、节假日调休等信息的日历显示，也可通过蓝牙传输图片至墨水屏作为电子相框使用。日历界面适配常见的 4.2 寸和 7.5 寸墨水屏分辨率，同一固件可驱动不同尺寸的屏幕（屏幕尺寸及驱动可通过网页端在线切换）。

## 支持的硬件

- **MCU**：`nrf51822` / `nrf51802` / `nrf52811` / `nrf52810`
- **墨水屏驱动**：`UC81xx` / `SSD16xx` 系列（黑白 / 三色 / 四色）
- **功能**：
  - 自定义引脚映射（墨水屏到 MCU）
  - 休眠 / 唤醒（NFC / 无线充电触发）
  - 蓝牙 OTA 固件升级

![](docs/images/3.jpg)

## 网页控制台

本项目提供了基于 Web Bluetooth API 的网页控制界面，可在手机或电脑上使用。

- 在线地址：https://tsl0922.github.io/EPD-nRF5
- 演示视频：https://www.bilibili.com/video/BV1KWAVe1EKs
- 交流群：[1033086563](https://qm.qq.com/q/SckzhfDxuu)

![](docs/images/0.jpg)

网页端支持多种图像抖动算法，可在图片上涂鸦、添加文字。除电子相框模式外，还可切换至日历模式，显示月历、农历节气、节假日及调休安排。

## 支持的设备

[查看设备列表](docs/devices.md)

## 项目目录结构

```
EPD-nRF5/
├── EPD/                    # 墨水屏驱动代码
│   ├── EPD_config.c/h      # 屏幕配置
│   ├── EPD_driver.c/h      # 驱动抽象层
│   ├── EPD_service.c/h     # BLE 墨水屏服务
│   ├── SSD16xx.c           # SSD16xx 系列驱动
│   └── UC81xx.c            # UC81xx 系列驱动
├── GUI/                    # 图形界面库
│   ├── Adafruit_GFX.c/h    # Adafruit GFX 图形库
│   ├── GUI.c/h             # 界面逻辑
│   ├── Lunar.c/h           # 农历计算
│   ├── fonts.c/h           # 字体
│   └── u8g2_font.c/h       # u8g2 字体
├── SDK/                    # Nordic SDK
│   ├── 12.3.0_d7731ad/     # 适用于 nRF51 系列
│   └── 17.1.0_ddde560/     # 适用于 nRF52 系列
├── Keil/                   # Keil MDK 工程文件
│   ├── EPD-nRF51.uvprojx   # nRF51 工程
│   ├── EPD-nRF52.uvprojx   # nRF52 工程
│   ├── DFU-nRF51.uvprojx   # nRF51 DFU 工程
│   └── DFU-nRF52.uvprojx   # nRF52 DFU 工程
├── docs/                   # 文档与数据手册
│   ├── images/             # 效果图
│   ├── datasheets/         # 芯片数据手册
│   └── OTP/                # OTP 寄存器配置
├── Makefile                # PC 端模拟器构建（GCC + MinGW）
└── emulator.c              # PC 端模拟器
```

## 开发指南

[查看开发文档](docs/develop.md)

### PC 端模拟器

项目提供了 Windows 端模拟器，可在 PC 上预览显示效果而无需硬件。

**编译要求：**
- GCC（MinGW）
- 链接库：gdi32

**构建与运行：**

```bash
# 编译
make

# 运行
./emulator.exe
```

**模拟器按键说明：**

| 按键 | 功能 |
|------|------|
| `←` `→` | 切换图片 / 月份 |
| `↑` `↓` | 调整亮度或对比度 |
| `W` `A` `S` `D` | 图片模式下移动显示区域 |
| `R` | 重置 |
| `Q` / `ESC` | 退出 |

## 致谢

本项目使用或参考了以下项目的代码：

- [ZinggJM/GxEPD2](https://github.com/ZinggJM/GxEPD2)
- [waveshareteam/e-Paper](https://github.com/waveshareteam/e-Paper)
- [atc1441/ATC_TLSR_Paper](https://github.com/atc1441/ATC_TLSR_Paper)

## 开源协议

本项目采用 MIT 协议开源，详见 [LICENSE](LICENSE) 文件。