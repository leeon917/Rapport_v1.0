# Rapport 前端 - HBuilderX 标准项目

本项目已转换为 HBuilderX 标准项目，使用 uni-app 内置编译器。

## 使用 HBuilderX 打开项目

1. 打开 HBuilderX
2. 文件 → 打开目录 → 选择本项目根目录
3. HBuilderX 会自动识别为 uni-app 项目

## 运行项目

### H5 网页版
1. 在 HBuilderX 中，点击工具栏"运行" → "运行到浏览器" → "Chrome"
2. 或使用快捷键：`Ctrl+R` (Windows) / `Cmd+R` (Mac)

### 微信小程序
1. 点击工具栏"运行" → "运行到小程序模拟器" → "微信开发者工具"
2. 需要先安装并配置微信开发者工具路径

## 项目结构

```
frontend/
├── src/                 # 源代码目录
│   ├── pages/          # 页面文件
│   ├── components/     # 组件文件
│   ├── api/            # API 接口
│   ├── store/          # Pinia 状态管理
│   ├── static/         # 静态资源
│   ├── App.vue         # 应用入口组件
│   ├── main.ts         # 程序入口文件
│   ├── pages.json      # 页面路由配置
│   └── manifest.json   # 应用配置文件
├── package.json        # 简化的依赖配置
└── tsconfig.json       # TypeScript 配置
```

## 后端 API 配置

后端地址在 `src/manifest.json` 的 `h5.devServer.proxy` 中配置：
- 本地后端: http://localhost:8000

## 注意事项

1. **不再需要命令行运行** - HBuilderX 会自动处理编译
2. **依赖管理** - HBuilderX 内置了 uni-app 所需的所有依赖
3. **图标资源** - `src/static/tabbar/` 中的图标是占位符，需要替换为实际图标

## CLI 版本备份

如果需要恢复 CLI 版本（Vite）：
- `package.json.cli.bak` - CLI 版本的依赖配置
- `vite.config.ts.bak` - Vite 配置文件

## 开发建议

- 使用 HBuilderX 内置的代码提示和自动补全
- 使用 HBuilderX 的条件编译功能处理多端差异
- 使用 HBuilderX 的真机调试功能测试 App
