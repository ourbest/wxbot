webpackJsonp([0],{25:function(t,e,a){a(85);var n=a(24)(a(70),a(96),"data-v-69cbbc0c",null);t.exports=n.exports},70:function(t,e,a){"use strict";Object.defineProperty(e,"__esModule",{value:!0}),e.default={data:function(){var t=this;return{total:0,columns:[{title:"发送者",key:"sender",width:120},{title:"文章",key:"title",render:function(t,e){var a=e.row;return t("a",{attrs:{href:"/bot/article?id="+a.id,target:"_blank"}},a.title)}},{title:"时间",key:"created_at",width:100},{title:"操作",width:250,key:"action",render:function(e,a){var n=a.row;return e("div",[e("Button",{props:{type:"text"},on:{click:function(){t.sendToCutt(n)}}},"发到发稿箱"),e("Button",{props:{type:"text"},on:{click:function(){t.$router.push({name:"article-editor",params:{uid:n.id}})}}},"编辑"),e("Button",{props:{type:"text"},on:{click:function(){t.removeArticle(n)}}},"删除")])}}],data:[],loadData:function(){var t=this;this.$http.get("/bot/articles",{params:{name:this.$route.params.bot,page:this.currentPage-1}}).then(function(e){t.data=e.data.articles,t.total=e.data.total})}}},computed:{currentPage:function(){return this.$route.params.page||1}},methods:{sendToCutt:function(t){this.$http.post()},removeArticle:function(t){var e=this;e.$Modal.confirm({content:"确认要删除【"+t.title+"】吗？",onOk:function(){e.$http.post("/bot/article/remove",{id:t.id}).then(function(){e.data.splice(e.data.indexOf(t),1)})}})},changePage:function(t){this.$router.push({name:"bot-articles-page",params:{page:t}})}},mounted:function(){this.loadData()},watched:{currentPage:function(){this.loadData()}}}},85:function(t,e){},96:function(t,e){t.exports={render:function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",[a("Table",{attrs:{columns:t.columns,data:t.data}}),t._v(" "),a("Page",{staticStyle:{"padding-top":"10px"},attrs:{total:t.total,current:t.currentPage,"show-elevator":"","page-size":100,size:"small"},on:{"on-change":t.changePage}})],1)},staticRenderFns:[]}}});