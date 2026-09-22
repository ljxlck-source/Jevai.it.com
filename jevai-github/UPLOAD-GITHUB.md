# 上传到 GitHub

1. 解压 `jevai-github.zip`。
2. 在 GitHub 新建一个空仓库，名称可用 `jevai`。
3. 进入仓库，选择 **uploading an existing file**，或 **Add file → Upload files**。
4. 打开解压后的 `jevai-github` 文件夹，将里面的文件和文件夹一起拖进去。不要只上传 ZIP，也不要把外层文件夹作为仓库中的额外一层。
5. 点击 **Commit changes** 完成上传。

仓库根目录应能看到 `README.md`、`vercel.json`、`dist`、`content`、`scripts`。隐藏的 `.gitignore` 如未拖进去，可用 Add file → Create new file 补上；不影响静态网站运行。

## 部署

上传 GitHub 仅保存文件，不会自动开通网站。

使用 Vercel 时导入这个仓库，Framework Preset 选择 Other，Output Directory 为 `dist`，不需要安装依赖或运行构建命令（已附生成后的网页）。在部署平台添加自定义域名 `jevai.it.com`，根据平台提供的记录配置 DNS。本站使用根路径链接，不能直接部署在 `/仓库名/` 子路径下。

## 修改内容

- 项目数据：`content/projects.json`。
- 英文文章：`content/*.md`。
- 导航与页面结构：`scripts/build.py`。
- 样式、交互及图标：`dist/assets/`，请保留这个目录。

修改内容后，在项目目录运行 `python3 scripts/build.py` 和 `python3 scripts/check.py`，将更新后的源码和 `dist` 一起上传。正常构建不需要原始 HTML；`extract_projects.py` 仅供以后重新导入原始项目列表时使用。

## 当前状态

左上角品牌名已改为 Jev.ai；实际配置域名仍为 jevai.it.com。包含 46 个项目、10 个分类及英文介绍内页。Google Analytics ID 为 G-6B7H863MFF，访客同意后加载。

原文章中的 17 个图片/视频资源仍待提供，当前页面没有放入失效占位图片。详见 content/media-manifest.json。此包未包含账号凭据、Git 历史或内部托管配置。
