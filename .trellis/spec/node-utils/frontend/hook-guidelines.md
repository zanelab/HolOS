# @vben/node-utils: Module-level "Hooks"

> 本包 has **no Vue hooks**. Read this as: how to plug a helper **into** an application's hook.

## 示例: use node-utils inside a Vue composable

When a Vue app wants to use `@vben/node-utils` helpers, wrap them in a `useXxx` composable in the **app**, not in 本包:

```ts
// apps/web-holos/src/composables/use-app-meta.ts
import { ref } from 'vue';
import { hash, formatBytes } from '@vben/node-utils';

export function useAppMeta() {
  const versionHash = ref<string>('');
  const sizeBytes = ref<number>(0);

  async function loadBuildMeta() {
    const res = await fetch('/__build_meta');
    const buf = new Uint8Array(await res.arrayBuffer());
    versionHash.value = hash(buf);
    sizeBytes.value = formatBytes(buf.byteLength);
  }

  return { versionHash, sizeBytes, loadBuildMeta };
}
```

## Where to use `@vben/node-utils` in this monorepo

- **Trellis scripts** (`.trellis/scripts/*.py`) — `git`, `monorepo`, `fs`, `path` are heavily used
- **Vite plugins / build tools** — `hash`, `formatter`, `spinner` for build diagnostics
- **Test runners** — `date` / `fs` for snapshot fixtures

## DON'T use it in

- Frontend runtime code that ships to the browser — it's a Node-only package (no fallback for browser globals).
- Vue composables that need reactivity — node-utils functions are not reactive; wrap them yourself if you need reactivity.

## 禁止

- ❌ Don't import `@vben/node-utils` from `apps/web-*/src/` if it ends up in the client bundle — check `vite.config.ts` tree-shaking.
- ❌ Don't call node-utils functions inside `setup()` without wrapping in a try/catch — they can throw on bad inputs.
- ❌ Don't add reactive wrappers directly in `@vben/node-utils` — keep it React/Vue-agnostic.
