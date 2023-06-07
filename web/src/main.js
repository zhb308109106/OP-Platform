import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import settings from '@/settings'
import Antd from 'ant-design-vue'
/**import 'ant-design-vue/dist/antd.css'**/
import ElementUI from 'element-plus';             //全局引入element
import 'element-plus/theme-chalk/index.css';    //全局引入element的样式
import Base64 from 'js-base64';
let echarts=require('echarts')
const debounce = (fn, delay) => {
  let timer = null;
  return function () {
    let context = this;
    let args = arguments;
    clearTimeout(timer);
    timer = setTimeout(function () {
      fn.apply(context, args);
    }, delay);
  }
}

const _ResizeObserver = window.ResizeObserver;
window.ResizeObserver = class ResizeObserver extends _ResizeObserver{
  constructor(callback) {
    callback = debounce(callback, 16);
    super(callback);
  }
}
const app = createApp(App)
app.use(store).use(router).use(ElementUI).use(Base64).mount('#app')
app.config.globalProperties.$settings = settings
app.config.globalProperties.$echarts = echarts
