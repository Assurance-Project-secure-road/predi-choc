if(!self.define){const e=e=>{"require"!==e&&(e+=".js");let r=Promise.resolve();return s[e]||(r=new Promise((async r=>{if("document"in self){const s=document.createElement("script");s.src=e,document.head.appendChild(s),s.onload=r}else importScripts(e),r()}))),r.then((()=>{if(!s[e])throw new Error(`Module ${e} didn’t register its module`);return s[e]}))},r=(r,s)=>{Promise.all(r.map(e)).then((e=>s(1===e.length?e[0]:e)))},s={require:Promise.resolve(r)};self.define=(r,i,n)=>{s[r]||(s[r]=Promise.resolve().then((()=>{let s={};const l={uri:location.origin+r.slice(1)};return Promise.all(i.map((r=>{switch(r){case"exports":return s;case"module":return l;default:return e(r)}}))).then((e=>{const r=n(...e);return s.default||(s.default=r),s}))})))}}define("./service-worker.js",["./workbox-8797399f"],(function(e){"use strict";e.setCacheNameDetails({prefix:"PrediChoc"}),self.addEventListener("message",(e=>{e.data&&"SKIP_WAITING"===e.data.type&&self.skipWaiting()})),e.precacheAndRoute([{url:"/css/642.7da821f5.css",revision:null},{url:"/css/847.b6fcae0a.css",revision:null},{url:"/css/app.238efb01.css",revision:null},{url:"/img/logo.53e8ab41.png",revision:null},{url:"/img/thuy.eb8c05aa.jpg",revision:null},{url:"/img/thuyqr.bdd27b85.png",revision:null},{url:"/img/yanice.359b7714.jpg",revision:null},{url:"/img/yaniceqr.63a47dbf.png",revision:null},{url:"/index.html",revision:"0f5bb069f74bd258b5f815fbe21e3585"},{url:"/js/642.49771d8c.js",revision:null},{url:"/js/847.409dde15.js",revision:null},{url:"/js/894.3e8253ee.js",revision:null},{url:"/js/app.441e4d89.js",revision:null},{url:"/js/chunk-vendors.8be89838.js",revision:null},{url:"/logo.svg",revision:"c730d96e4ca196169a3755b25764e4a9"},{url:"/manifest.json",revision:"55a8fc94c7a1e251074a7d069c071b45"},{url:"/robots.txt",revision:"b6216d61c03e6ce0c9aea6ca7808f7ca"}],{})}));
//# sourceMappingURL=service-worker.js.map