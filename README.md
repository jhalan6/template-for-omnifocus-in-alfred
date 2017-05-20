# template-for-omnifocus-in-alfred

qof 是一个自定义omnifocus模板的alfred插件，目的是解决常用的omnifocus任务的导入。

### 功能
- 通过json配置自动导入任务的熟悉
- 支持子任务（通过文本配置、脚本获取）
- 支持定义导入任务标记
- 支持向所有项目、inbox、folder中添加任务
- 支持自定义变量名
### 使用
- 安装
	`make && open qof.alfredworkflow`
- 配置
	复制.quick\_of文件夹到\~目录
- 示例
	在alfred 中输入 qof book
	![][image-1]
	显示的标题book表示这个自定义模板的名称，副标题为配置文件中设置的解析方式，如下图所示
	![][image-2]
	即表示已book这个模版来解析从alfred中传入的参数，其中，”浪潮之巅”会被解析为bookName;”25”会被解析为chapterNum。
	键入回车后，就开始按照模板定义的方式生成了omnifocus中的一个任务
	![][image-3]
- 配置分析
	`{"book":{ "parse": "bookName chapterNum" , "name": "$bookName", "child task": "!python book\_child.py $chapterNum", "inbox": false , "sequential": true, "folder":"读书","flagged": false}}`
	- parse: 解析参数的方式，在alfred 中，配置名后面的参数会按照这里设置的名称进行解析。
	- name: 创建的任务的名称，可以使用解析出来的变量值，通过$引用变量值
	- child task:子任务列表。通过\\n进行分割。可以使用!开头，表示是需要执行的脚本，会在\~/.quick\_of 目录下发起执行，并将执行结果作为子目录的列表。
	- inbox: 指定是否创建在inbox中
	- sequential:指定任务的完成顺序，true为顺序执行，
	- folder：指定task最终加入到哪个目录中
	- flagged: 是否打标记，true为打标记


[image-1]:	https://oeu8f0i18.qnssl.com/Screen%20Shot%202017-05-20%20at%2018.16.10.png "qof 示例"
[image-2]:	https://oeu8f0i18.qnssl.com/Screen%20Shot%202017-05-20%20at%2018.19.20.png
[image-3]:	https://oeu8f0i18.qnssl.com/qof_book_result_demo.png "导入结果"