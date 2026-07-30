# @vben/backend-mock Component Guidelines

> Nitro Mock Server "Components" = HTTP endpoints.

## Pattern: defineEventHandler

```ts
import { defineEventHandler, readBody, createError } from "h3";
export default defineEventHandler(async (event) => {
  const body = await readBody(event);
  if (!body.username) throw createError({ statusCode: 400 });
  return { access_token: "mock-token" };
});
```

## Forbidden

- Don't use Express
- Don't use Generators
