webpackJsonp([2],{55:function(e,t,n){n(72);var o=n(20)(n(64),n(81),"data-v-712669fa",null);o.options.__file="/Users/wangk/git/wxbot-fe/src/views/bot-mps.vue",o.esModule&&Object.keys(o.esModule).some(function(e){return"default"!==e&&"__esModule"!==e})&&console.error("named exports are not supported in *.vue files."),o.options.functional&&console.error("[vue-loader] bot-mps.vue: functional components are not supported with templates, they should use render functions."),e.exports=o.exports},64:function(e,t,n){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),t.default={data:function(){return{columns:[{title:"名称",key:"name",width:120},{title:"性别",key:"sex",width:60},{title:"省份",key:"province",width:100},{title:"城市",width:100,key:"city"},{title:"备注",width:120,key:"remark_name"},{title:"签名",key:"signature"}],data:[]}},mounted:function(){var e=this;this.$http.get("/bot/mps",{params:{name:this.$route.params.bot}}).then(function(t){e.data=t.data.mps})}}},72:function(e,t){},81:function(e,t,n){e.exports={render:function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",[n("Table",{attrs:{columns:e.columns,data:e.data}})],1)},staticRenderFns:[]},e.exports.render._withStripped=!0}});