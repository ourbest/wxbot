webpackJsonp([2],{63:function(t,e,n){n(80);var a=n(24)(n(72),n(89),"data-v-712669fa",null);t.exports=a.exports},72:function(t,e,n){"use strict";Object.defineProperty(e,"__esModule",{value:!0}),e.default={data:function(){return{columns:[{title:"名称",key:"name",width:120},{title:"省份",key:"province",width:100},{title:"城市",width:100,key:"city"},{title:"备注",width:120,key:"remark_name"},{title:"签名",key:"signature"}],data:[]}},mounted:function(){var t=this;this.$http.get("/bot/mps",{params:{name:this.$route.params.bot}}).then(function(e){t.data=e.data.mps})}}},80:function(t,e){},89:function(t,e){t.exports={render:function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",[n("Table",{attrs:{columns:t.columns,data:t.data}})],1)},staticRenderFns:[]}}});