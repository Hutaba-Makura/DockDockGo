/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_PUBLIC_API_BASE: string
  // 他の環境変数があればここに追加
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
