webpackJsonp([11],{106:function(t,e){t.exports={render:function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",[n("Table",{attrs:{columns:t.columns,data:t.data}})],1)},staticRenderFns:[]}},67:function(t,e,n){n(92);var a=n(11)(n(80),n(106),"data-v-1030c530",null);t.exports=a.exports},80:function(t,e,n){"use strict";Object.defineProperty(e,"__esModule",{value:!0}),e.default={data:function(){return{columns:[{title:"名称",key:"name",width:120},{title:"性别",key:"sex",width:60},{title:"省份",key:"province",width:100},{title:"城市",width:100,key:"city"},{title:"备注",width:120,key:"remark_name"},{title:"签名",key:"signature"}],data:[]}},mounted:function(){var t=this;this.$http.get("/bot/friends",{params:{name:this.$route.params.bot}}).then(function(e){t.data=e.data.friends})}}},92:function(t,e){}});