webpackJsonp([6],{105:function(t,e){t.exports={render:function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",[n("Table",{attrs:{columns:t.columns,data:t.data}})],1)},staticRenderFns:[]}},69:function(t,e,n){n(92);var a=n(11)(n(81),n(105),"data-v-712669fa",null);t.exports=a.exports},81:function(t,e,n){"use strict";Object.defineProperty(e,"__esModule",{value:!0}),e.default={data:function(){return{columns:[{title:"名称",key:"name",width:120},{title:"省份",key:"province",width:100},{title:"城市",width:100,key:"city"},{title:"备注",width:120,key:"remark_name"},{title:"签名",key:"signature"}],data:[]}},mounted:function(){var t=this;this.$http.get("/bot/mps",{params:{name:this.$route.params.bot}}).then(function(e){t.data=e.data.mps})}}},92:function(t,e){}});