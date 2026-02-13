import { createSSRApp } from 'vue';
import * as Pinia from 'pinia';
import App from './App.vue';

export function createApp() {
  const app = createSSRApp(App);

  // 使用Pinia
  const pinia = Pinia.createPinia();
  app.use(pinia);

  return {
    app,
    pinia
  };
}
