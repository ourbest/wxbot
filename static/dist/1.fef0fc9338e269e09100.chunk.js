webpackJsonp([1],{56:function(t,e,n){n(69);var s=n(20)(n(65),n(78),"data-v-14719ca0",null);t.exports=s.exports},65:function(t,e,n){"use strict";Object.defineProperty(e,"__esModule",{value:!0}),e.default={computed:{menu:function(){var t=this.$route.path;return t.substr(t.lastIndexOf("/")+1)},bot:function(){return this.$route.params.bot}},methods:{openInfo:function(t){this.$router.push({name:"bot-"+t,params:{bot:this.bot}})}}}},69:function(t,e){},78:function(t,e){t.exports={render:function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",[n("h2",[t._v("机器人 【"+t._s(t.bot)+"】")]),t._v(" "),n("Menu",{attrs:{mode:"horizontal","active-name":t.menu},on:{"on-select":t.openInfo}},[n("Menu-item",{attrs:{name:"info"}},[t._v("基本信息")]),t._v(" "),n("Menu-item",{attrs:{name:"friends"}},[t._v("好友")]),t._v(" "),n("Menu-item",{attrs:{name:"mps"}},[t._v("公众号")]),t._v(" "),n("Menu-item",{attrs:{name:"groups"}},[t._v("群聊")]),t._v(" "),n("Menu-item",{attrs:{name:"messages"}},[t._v("消息")]),t._v(" "),n("Menu-item",{attrs:{name:"articles"}},[t._v("文章")])],1),t._v(" "),n("div",{staticClass:"margin"},[n("router-view")],1)],1)},staticRenderFns:[]}}});