## Memo on how to deal with multi projects on jean-zay@IDRIS

* `idrproj` to see how many projects your account is related to:
```
regi915@jean-zay3:>> idrproj 

Available projects:
-------------------
  cli (90727/A0090112020) 
  egi (91279/A0100101279) [default][active]
  bcn (101593/A0090112071) 
```

* To switch from one project to another:
```
regi915@jean-zay3:>>  eval $(idrenv -d cli)
```

*  The full documentation on the IDRIS website: [[FR]](http://www.idris.fr/jean-zay/cpu/jean-zay-cpu-doc_multi_projet.html) / [[EN]](http://www.idris.fr/eng/jean-zay/cpu/jean-zay-cpu-doc_multi_projet-eng.html)
