webpackJsonp([8],{102:function(t,e){},115:function(t,e){t.exports={render:function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",[a("Table",{attrs:{columns:t.columns,data:t.data}})],1)},staticRenderFns:[]}},70:function(t,e,a){a(102);var n=a(11)(a(83),a(115),"data-v-d41b9cee",null);t.exports=n.exports},83:function(t,e,a){"use strict";Object.defineProperty(e,"__esModule",{value:!0}),e.default={data:function(){return{columns:[{title:"聊天",key:"chat",width:120},{title:"发送者",key:"sender",width:120},{title:"类型",key:"type",width:80},{title:"消息",key:"message"},{title:"时间",key:"created_at",width:100}],data:[]}},mounted:function(){var t=this;this.$http.get("/bot/messages",{params:{name:this.$route.params.bot}}).then(function(e){t.data=e.data.messages})}}}});