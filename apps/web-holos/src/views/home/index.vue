<script lang="ts" setup>
import { useI18n } from 'vue-i18n';

const { t } = useI18n();
</script>

<template>
  <div class="holos-home">
    <header class="holos-home__header">
      <h1 class="holos-home__title">HolOS</h1>
      <p class="holos-home__subtitle">{{ t('page.home.tagline') }}</p>
    </header>

    <section class="holos-home__content">
      <div class="holos-home__placeholder">
        <span class="holos-home__dot" />
        <span class="holos-home__dot" />
        <span class="holos-home__dot" />
      </div>
      <p class="holos-home__hint">{{ t('page.home.ready') }}</p>
    </section>
  </div>
</template>

<style scoped>
.holos-home {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100%;
  padding: 48px 24px;
  text-align: center;
  gap: 32px;
}

.holos-home__header {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.holos-home__title {
  font-size: 64px;
  font-weight: 800;
  letter-spacing: -0.04em;
  margin: 0;
  background: linear-gradient(135deg, #00ff41 0%, #00b8d4 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  color: transparent;
}

.holos-home__subtitle {
  font-size: 18px;
  color: rgba(255, 255, 255, 0.6);
  margin: 0;
  font-weight: 400;
}

.holos-home__content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 24px;
}

.holos-home__placeholder {
  display: flex;
  gap: 12px;
}

.holos-home__dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #00ff41;
  opacity: 0.4;
  animation: holos-blink 1.4s infinite;
}

.holos-home__dot:nth-child(2) {
  animation-delay: 0.2s;
}

.holos-home__dot:nth-child(3) {
  animation-delay: 0.4s;
}

.holos-home__hint {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.4);
  margin: 0;
  font-family: 'SF Mono', Menlo, Consolas, monospace;
}

@keyframes holos-blink {
  0%, 60%, 100% { opacity: 0.4; }
  30% { opacity: 1; }
}
</style>
