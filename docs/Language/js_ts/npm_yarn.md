# 设置代理 (clash)

- npm

```bash
npm config set proxy http://127.0.0.1:7890
npm config set https-proxy https://127.0.0.1:7890
```

- yarn v1

```bash
yarn config set proxy http://127.0.0.1:7890
yarn config set https-proxy https://127.0.0.1:7890
```

- yarn v2 (add into the .yarnrc.yml of project)

```
httpProxy: http://127.0.0.1:7890
httpsProxy: https://127.0.0.1:7890
```

# 镜像源

```bash
    // 查询源
    yarn config get registry

    // 更换国内源
    yarn config set registry https://registry.npmmirror.com
    yarn config get registry

    // 恢复官方源
    yarn config set registry https://registry.yarnpkg.com
    yarn config get registry



	// 删除注册表
    yarn config delete registry
```

# 查看代理

```bash
npm config get proxy
npm config get https-proxy


yarn config get proxy
yarn config get https-proxy


```

# 删除

```bash

yarn config delete proxy
yarn config delete https-proxy

npm config delete proxy
npm config delete https-proxy

```

### vesrion

- 更新

```
npm update
```

```
yarn upgrade
```

### 代码格式化

```
yarn add eslint
```

### 根据openapi.json自动生成client

```shell
yarn add openapi-typescript-codegen --save-dev
```

```shell
npx openapi-typescript-codegen --input http://localhost:5000/api/v1/openapi.json --output ./src/api

```
