webpackJsonp([4],{53:function(t,n,o){o(67);var e=o(20)(o(62),o(76),"data-v-0a1fae6b",null);t.exports=e.exports},62:function(t,n,o){"use strict";Object.defineProperty(n,"__esModule",{value:!0}),n.default={data:function(){return{info:""}},computed:{bot:function(){return this.$route.params.bot}},methods:{logoutBot:function(){var t=this;this.$http.get("/bot/logout",{params:{name:this.bot}}).then(function(){t.$router.push("/")})}},mounted:function(){var t=this;this.$http.get("/bot/info",{params:{name:this.bot}}).then(function(n){t.info=n.data.friends})}}},67:function(t,n){},76:function(t,n){t.exports={render:function(){var t=this,n=t.$createElement,o=t._self._c||n;return o("div",[o("pre",[t._v(t._s(t.info))]),t._v(" "),o("Button",{attrs:{type:"primary"},on:{click:t.logoutBot}},[t._v("注销")])],1)},staticRenderFns:[]}}});