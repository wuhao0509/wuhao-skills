#Vue面经

[[第一章 权衡的艺术]]
[[第二章 框架设计核心要素]]
[[第三章 Vue.js 3的设计思路]]

[你都知道哪些Vue3.0的新特性？](https://github.com/57code/vue-interview/blob/master/public/18-v3-feature/README.md)
- 面试官：Vue3.0 性能提升主要是通过哪几方面体现的？7点 [题解](https://github.com/febobo/web-interview/issues/46) ^66d66f7e-bec6-4936-859c-fd645fd904a0
	- Tree Shaking
	- Composition API（提高代码复用性，减少组件间的耦合），自定义渲染器更易扩展
	- 响应式（Proxy）
	- 组件更新：Diff算法、事件绑定优化（patchProps时将事件处理函数绑定到了一个invoker上）
	- 编译优化：动态节点收集（patchFlags、Block树）、字符串处理（静态提升、预字符串化）、缓存（事件处理函数、v-once）
	- 更好的TS支持
	- 内置异步组件Suspense

[你了解哪些Vue性能优化方法？](https://github.com/57code/vue-interview/blob/master/public/08-vue-perf/README.md)
- 略 ^66cc726b-e813-423f-bc72-43dfa689c1d9

[说说你对虚拟 DOM 的理解？](https://github.com/57code/vue-interview/blob/master/public/20-vdom/README.md)
- 虚拟dom本身就是一个 `JavaScript` 对象
-
- 通过引入vdom我们可以获得如下好处
	- 减少直接操作 dom 次数，从而提高程序性能，频繁的dom操作容易引起页面的重绘和回流
	- Vue3 中允许开发者基于 VNode 实现自定义渲染器（renderer），以便于针对不同平台进行渲染。
		- 同一 VNode 节点可以渲染成不同平台上的对应的内容，比如：渲染在浏览器是 dom 元素节点，渲染在 Native变为对应的控件、可以实现 SSR
		-
- vdom如何生成
	- [[一 Vue框架设计#^66c9da55-0766-452f-94ce-52e29d13112b]]
-
- vdom最终去哪
	- [[一 Vue框架设计#^66c9da54-0d0e-4fa0-bad3-574569991dde]]
-
- 挂载过程结束后，vue程序进入更新流程。如果某些响应式数据发生变化，将会引起组件重新render，此时就会生成新的vdom，和上一次的渲染结果diff就能得到变化的地方，从而转换为最小量的dom操作，高效更新视图

[面试官：Vue3.0 所采用的 Composition Api 与 Vue2.x 使用的 Options Api 有什么不同？(opens new window)](https://github.com/febobo/web-interview/issues/48)
- 逻辑组织
	- Vue2：这种碎片化使得理解和维护复杂组件变得困难
	- Vue3：将某个逻辑关注点相关的代码全都放在一个函数里，这样当需要修改一个功能时，就不再需要在文件中跳来跳去
- 逻辑复用
	- vue2过去使用mixin，一个组件引入多个mixin，会导致两个问题
		- 命名冲突
		- 数据来源不清晰
	- vue3：data、computed、watch等都被封装到一个hook（函数）里，父组件模块化导入，不会出现命名冲突的问题
-

[面试官：说说Vue 3.0中Treeshaking特性？举例说明一下？(opens new window)](https://github.com/febobo/web-interview/issues/67)
- Vue TreeShaking是基于Rollup实现的，`Tree shaking`是基于`ES6`模块化，他可以在编译阶段静态分析导入的代码，并将排除任何实际上没有使用的内容
-
- Vue2：核心API全部引入
- Vue3：核心API可以按需引入
-
- [[一 Vue框架设计#^66c9da54-e57a-4dc1-bcc2-c16c19159c80]]
-

[面试官：说说你对SPA（单页应用）的理解?(opens new window)](https://github.com/febobo/web-interview/issues/3)
- SPA与MPA的区别
	- | |单页面应用（SPA） | 多页面应用（MPA） |
	  | ---- | ---- |
	  | 组成 | 一个主页面和多个页面片段 | 多个主页面 |
	  | 刷新方式 | 局部刷新 | 整页刷新 |
	  | url模式 | 哈希模式 | 历史模式 |
	  | SEO搜索引擎优化 | 难实现，可使用SSR方式改善 | 容易实现 |
	  | 数据传递 | 容易 | 通过url、cookie、localStorage等传递 |
	  | 页面切换 | 速度快，用户体验良好 | 切换加载资源，速度慢，用户体验差 |
	  | 维护成本 | 相对容易 | 相对复杂 |
- 如何给SPA做SEO
	- SSR

[面试官：SPA（单页应用）首屏加载速度慢怎么解决？?(opens new window)](https://github.com/febobo/web-interview/issues/8)
[面试官：SSR解决了什么问题？有做过SSR吗？你是怎么做的？(opens new window)](https://github.com/febobo/web-interview/issues/27)
- 结合项目：H5SSR采用流式渲染，MRN跨端框架就是正常接入SSR




死区
[面试官：说说你对vue的理解?(opens new window)](https://github.com/febobo/web-interview/issues/1)
[面试官：什么是虚拟DOM？如何实现一个虚拟DOM？说说你的思路(opens new window)](https://github.com/febobo/web-interview/issues/23)
[SPA、SSR的区别是什么](https://github.com/57code/vue-interview/blob/master/public/31-SPA-SSR/README.md)