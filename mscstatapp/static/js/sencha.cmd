sencha -sdk "C:\senchaextjs\ext-6.2.0" generate app -ext -classic MSCSTAT "d:\Works\Developers\PycharmProjects\mscstat\mscstatapp\static\js\sencha_new"
sencha app upgrade "C:\senchaextjs\ext-6.2.0"
sencha app refresh
sencha app build production
sencha app build testing
sencha app build --clean development
sencha app watch