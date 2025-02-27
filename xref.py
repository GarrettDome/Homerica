#!/usr/bin/env python3
  
import sys
import re

from lxml import etree
from greek_accentuation.characters import *
from greek_accentuation.syllabify import *
from greek_accentuation.accentuation import *

lemmaids = {}
id2lemma = {}
allids = {}
precid = {}
nextid = {}
preclemma = {}
nextlemma = {}
curid = ''
lastid = ''
curnumber = ''
terms = 0

def procxref(greektag,secref,curl,errmess):
      greektag = re.sub('[<]','',greektag)
      greektag1 = greektag
      greektag = re.sub('(.)\-([^0-9])','\g<1>\g<2>',greektag)
      if( greektag == "ἡ" or greektag == "τό" or greektag == "ὁ"):
       return(curl)

      if( greektag not in lemmaids and re.search(r'[0-9]$',greektag)):
       newtag = re.sub(r'[0-9]+$','',greektag)
       newnum = re.sub(r'.+[^0-9]([0-9]+)$','\g<1>',greektag)
       newfulltag = newtag + '-' + newnum
       if( newtag in lemmaids):
         sys.stderr.write("nonumhit1\t"+newtag+"\t"+newnum+"\t"+curl)
         newfulltag = lemmaids[newtag] + '-' + newnum
         if( newfulltag in allids):
           sys.stderr.write("nonumhit2\t"+newtag+"\t"+newnum+"\t"+curl)
           curl = re.sub('<foreign xml:lang="greek">'+greektag1+'</foreign>','<ref xml:lang="greek" target="' + newfulltag + '"><foreign xml:lang="greek">' + newtag + "</foreign> " + str(newnum) + '</ref>',curl)
           return(curl)
         else:
           sys.stderr.write("nonumhit-fail\t"+greektag+"\t"+newtag+"\t"+newnum+"\t"+curl)
       
      if( greektag not in lemmaids):
        if( not re.search(r'-$',greektag) and not re.search(r'^-',greektag) and not re.search('ϝ',greektag)):
         sys.stderr.write(errmess+"\t"+greektag+"\t"+curl)
      else:
       curl = re.sub('<foreign xml:lang="greek">'+greektag1+'</foreign>','<ref xml:lang="greek" target="' + lemmaids[greektag] + '">' + greektag1 + '</ref>',curl)
       #print("newcurl",curl)
      return(curl)

lexfile = "cunliffe.lexentries.unicode.xml"
with open(lexfile) as f:
  for line in f:
    line = re.sub('†','',line)
    line = re.sub('\*','',line)
    m = re.search(r'(?<=xml:id=")[^"]+[lf][ei][x]"',line)
    curnumber = ''
    if(m):
      curid = m.group(0)
      curid = re.sub('"','', curid)
      precid[curid] = lastid
      nextid[lastid] = curid
      sys.stderr.write('setprecid\t'+"prec:"+curid+'\t'+"cur:"+lastid+'\n')
      curlemma = ''
     # print("newid",curid)
    m = re.search(r'(?<=xml:id=")[^"]+[lf][ei][x][^"]+',line)
    if(m):
      tmpid = m.group(0)
      allids[tmpid] = 1
      sys.stderr.write('setallids\t' + 'curid' + '\t' + tmpid + '\n')
    m = re.search(r'(?<=<head><foreign xml:lang="greek">)[^<]+',line)
    if(m and curid):
      tl = curlemma
      curlemma = m.group(0)
      preclemma[curlemma] = tl
      nextlemma[tl] = curlemma
     # print("curlem",curlemma)
    m = re.search(r'<bibl',line)
    m1 = re.search(r'\-prefix',curid)
    m2 = re.search(r'\-suffix',curid)
    if( ( m or m1 or m2) and curid and curlemma):
      lemmaids[curlemma] = curid
      id2lemma[curid] = curlemma
     # print("lemmaid",lemmaids[curlemma],curlemma)
      lastid = curid
      curid = ''
f.close()

if( curid and curlemma):
      lemmaids[curlemma] = curid
      #print("lemmaid",lemmaids[curlemma],curlemma)
      lastid = curid
      curid = ''

lemmaids['πολύς'] = "pollos-cunliffe-lex"
lemmaids['τάμνω'] = "temno-cunliffe-lex"
lemmaids['ὀρέγνυμι'] = "orego-cunliffe-lex"
lemmaids['ὅς1'] = "heos-cunliffe-lex"
lemmaids['τίω'] = "tio-cunliffe-lex"
lemmaids['δείδια'] = "deidoica-cunliffe-lex"
lemmaids['ἔργω2'] = "erdo-cunliffe-lex"
lemmaids['μέσσος'] = "mesos-cunliffe-lex"
lemmaids['πτόλεμος'] = "polemos-cunliffe-lex"
lemmaids['λήθω'] = "lanthano-cunliffe-lex"
lemmaids['αἰεί'] = "aiei-cunliffe-lex"
lemmaids['ὀπίσω'] = "opisso-cunliffe-lex"
lemmaids['ὄπιθε'] = "opisthe-cunliffe-lex"
lemmaids['ἐξ-'] = "ec-cunliffe-prefix"
lemmaids['ἐνέπω'] = "ennepo-cunliffe-lex"
lemmaids['δίημι'] = "diemai-cunliffe-lex"
lemmaids['σκοπιάομαι'] = "scopiazo-cunliffe-lex"
lemmaids['πλώω'] = "pleo-cunliffe-lex"
lemmaids['οὖς'] = "ouas-cunliffe-lex"
lemmaids['ὄνυμα'] = "onoma-cunliffe-lex"
lemmaids['πτόλις'] = "polis-cunliffe-lex"
lemmaids['τάμνω'] = "tamno-cunliffe-lex"

lexfile = "cunliffe.lexentries.unicode.xml"
with open(lexfile) as f:
  for line in f:
    line = re.sub('([\.\;,:])(</foreign>)','\g<2>\g<1>',line)
    line = re.sub(r'\+[ ]+','+ ',line)
    line = re.sub('ς-<', 'σ-<',line)
    line = re.sub('ς-"', 'σ-"',line)
    line = re.sub('>\+<', '> + <',line)
    line = re.sub('<p>[ ]+','<p>',line)
    line = re.sub(r'–[ ]*(<\/p>)','\g<1>',line)

    line = re.sub(r'\=[ ]*<cit><quote xml:lang="greek">([^<]+)<\/quote>[ ]*(<bibl[^>]+>[^<]+<\/bibl>)<\/cit>','= <foreign xml:lang="greek">\g<1></foreign> \g<2>',line)

    

    m = re.search(r'<foreign xml:lang="greek">([^<]+)</foreign>[ ]+<ref>([^<])+</ref>',line)
    #if(m):
     #print("compxref",m[1],m[2])

    if ( re.search('\[',line)):
     #sys.stderr.write("deriv" + "\t" + line)
     m = re.search(r'(?<=<foreign xml:lang="greek">)[^\-][^ϝ <]+<',line)
     if(m):
      line = procxref(m.group(0),'',line,"badxref50")

     m = re.search(r'(?<=<foreign xml:lang="greek">)[^\-][^ϝ <]+<',line)
     if(m):
      line = procxref(m.group(0),'',line,"badxref50")

     m = re.search(r'(?<=<foreign xml:lang="greek">)[^\-][^ϝ <]+<',line)
     if(m):
      line = procxref(m.group(0),'',line,"badxref50")
      

     m = re.search(r'(?<=<foreign xml:lang="greek">)[^\-][^ϝ <]+<',line)
     if(m):
      line = procxref(m.group(0),'',line,"badxref50")
      
      
    m = re.search(r'(?<=<foreign xml:lang="greek">)[^ <]+<\/foreign><\/ref>',line)
    if(m):
      works = m.group(0)
      works = re.sub('</foreign></ref>','',works)
      line = re.sub(r'<ref>(<foreign[^>]+>[^<]+<\/foreign>)<\/ref>','\g<1>',line)
      line = procxref(works,'',line,"badxref62")

    m = re.search(r'(?<=\[<foreign xml:lang="greek">)[^ <]+<',line)
    if(m):
      line = procxref(m.group(0),'',line,"badxref10")
      
    m = re.search(r'(?<=[Ff]or <foreign xml:lang="greek">)[^ <]+<',line)
    if(m):
      line = procxref(m.group(0),'',line,"badxref1")

    m = re.search(r'(?<=[Ss]ee <foreign xml:lang="greek">)[^ <]+<',line)
    if(m):
      line = procxref(m.group(0),'',line,"badxref1")

    m = re.search(r'(?<=[Ll]ike <foreign xml:lang="greek">)[^ <]+<',line)
    if(m):
      line = procxref(m.group(0),'',line,"badxref13")

    m = re.search(r'(?<=[Ww]ith <foreign xml:lang="greek">)[^ <]+<',line)
    if(m):
      line = procxref(m.group(0),'',line,"badxref2")

    m = re.search(r'(?<=form of <foreign xml:lang="greek">)[^ <]+<',line)
    if(m):
      line = procxref(m.group(0),'',line,"badxref2")

    m = re.search(r'(?<=\<ref><foreign xml:lang="greek">)[^ <]+<',line)
    if(m):
      line = procxref(m.group(0),'',line,"badxref20")

    m = re.search(r'(?<=\+ <foreign xml:lang="greek">)[^ <]+<',line)
    if(m):
      line = procxref(m.group(0),'',line,"badxref2")

    m = re.search(r'(?<=[Uu]nder <foreign xml:lang="greek">)[^ <]+<',line)
    if(m):
      line = procxref(m.group(0),'',line,"badxref1")

    line = re.sub(r'=<foreign','= <foreign',line)

    m = re.search(r'(?<=[=,] <foreign xml:lang="greek">)[^ <]+<',line)
    if(m):
      line = procxref(m.group(0),'',line,"badxref1")

    m = re.search(r'(?<=-</foreign>, <foreign xml:lang="greek">)[^ <]+[^\-]<',line)
    if(m):
      line = procxref(m.group(0),'',line,"badxref1")

    m = re.search(r'(?<=[CcFf][rf]\. <foreign xml:lang="greek">)[^ <]+<',line)
    if(m):
      line = procxref(m.group(0),'',line,"badxref1")

    m = re.search(r'(?<=[Tt]he <foreign xml:lang="greek">)[^ <]+<',line)
    if(m):
      line = procxref(m.group(0),'',line,"badxref1")

    m = re.search(r'(?<=<\/ref>, <foreign xml:lang="greek">)[^ <]+<',line)
    if(m):
      line = procxref(m.group(0),'',line,"badxref1")

    line = re.sub(r'<ref>(<ref xml:lang=[^>]+>[^<]+</ref>)</ref>','\g<1>',line)

    if( re.search('xml:id="[^"]+cunliffe-lex"',line)):
      m = re.search(r'(?<=xml:id=")[^"]+',line)
      curid = m.group(0)

    if( re.search(r'\bprec[\.]+',line)):
       if( curid in precid):
        sys.stderr.write('precid\t'+curid+"\t"+precid[curid]+"\t"+id2lemma[precid[curid]]+"\n")
        subs = '<ref target="' + precid[curid] + '" n="prec">' + id2lemma[precid[curid]] + '</ref>.'
        line = re.sub(r'\bprec[\.]+',subs,line)
       else:
        sys.stderr.write('precid\t'+curid+"\tnocurid\n")
        
    if( re.search(r'\bnext[\.]+',line)):
       if( curid in nextid):
        subs = '<ref target="' + nextid[curid] + '" n="next">' + id2lemma[nextid[curid]] + '</ref>.'
        line = re.sub(r'\bnext[\.]+',subs,line)
        sys.stderr.write('nextid\t'+curid+"\t"+nextid[curid]+"\t"+id2lemma[nextid[curid]]+"\n")
       else:
        sys.stderr.write('nextid\t'+curid+"\tnocurid\n")
        

    m = re.search(r'<p>[123][ ]+(sing\.|pl\.|dual)',line)
    if( m):
       curnumber = m.group(1)
       sys.stderr.write('setcurnumber\t'+curnumber+'\n')

    if( curnumber and re.search('<p>[123]\s+<',line)):
      line = re.sub(r'<p>([123])\s+<','<p>\g<1> '+curnumber + ' <',line)

    subpat1 = '(<p>|<p>\s*Also\s+|<p>\s*Elsewhere\s+|<p>\s*In\s+|<p>So in\s+|<p>\s*With\s+|<p>As\s+|<p>\[|\s+as\s+|\s+in\s+|\s+with\s+)'
    subpat2 = '([Pp]ron\.|[Tt]rans\.|[Ii]ntrans\.|[Aa]dvbs\.|[Ii]nt\.|[Aa]dverb|[Ss]b\.|[Nn]eg\.|sigmatic|[Pp]rep\.|[Aa]djectivally|[Dd]esiderative|[Aa]dv\.|[Cc]omplementary|cognate\s+acc\.|double\s+acc\.|[Aa]ugment|[Ii]mpers\.|[Ss]ing|[Ss]b\.|[Nn]eut\.|[Ss]uperl\.|[Cc]omp\.|[Aa]ct\.|[Pp]ass\.|[Aa]bsol\.|[Ii]mpf\.|[Ii]nstrument|[Nn]on.thematic|[123]\s+sing|[Aa]or\.|[Mm]id\.|[Pp]ple|[123]\s+pl\.|[123]\s+dual|[Nn]om\.|[Gg]en\.|[Gg]enit\.|[Dd]at\.|[Aa]cc\.|[Ff]em\.|[Ii]nfin|[Ff]ut.|[Pp]l\.|[Ii]terat\.|[Pp]a\.|[Ss]ubj\.|[Oo]pt\.|[Cc]ontr\.|[Pp]ass\.|[Pp]f\.|[rR]edup\.|[123]\s+and\s+|[Pp]res\.|[Pp]lupf\.|[Vv]oc\.|[Ii]mp\.|Locative)'

    subpat = '(</foreign>,|</ref>[,]*|</cit>[\)\.]|</bibl>[\)\.]|etc\.|\)\.|\.\)|\.\–)[ ]+' + subpat2 + '([^<]*)([ ]*)'
    line = re.sub(subpat,"\g<1></p>\n<p>\g<2>\g<3>\g<4>",line)

    subpat = subpat1 + subpat2  + '([^<]*)[ ]+'
    if( re.search(subpat,line)):
     line = re.sub(subpat,'\g<1><term>\g<2>\g<3></term> ',line)
     terms = terms + 1

    subpat = subpat1 + subpat2  + '([<]*)'
    if( re.search(subpat,line)):
     line = re.sub(subpat,'\g<1><term>\g<2></term>\g<3>',line)
     terms = terms + 1

    line = re.sub(r'</term>[ ]+'+subpat2,' \g<1></term>',line)

    line = re.sub(r'\s+See</term>','</term> See',line)

    m = re.search(r'(?<=<\/term> <foreign xml:lang="greek">)[^\-][^ϝ <]+[^\-]<',line)
    if(m):
      line = procxref(m.group(0),'',line,"badxref55")
      

#  <p>[<ref xml:lang="greek" target="amphi-cunliffe-prefix">ἀμφι-</ref> <ref>1</ref> <ref>3</ref>.]</p>
    if( re.search('(<ref xml:lang=[^>]+>[^<]+<\/ref>)[ ]*(<ref>[0-9]+<\/ref>)[ ]+(<ref>[0-9]+<\/ref>)',line)):
     sys.stderr.write('befores\t'+line)
     line = re.sub('(<ref xml:lang=[^>]+>[^<]+<\/ref>)[ ]*(<ref>[0-9]+<\/ref>)[ ]+(<ref>[0-9]+<\/ref>)','\g<1> \g<2>, \g<1> \g<3>',line)
     sys.stderr.write('afters\t'+line)
    while( re.search(r'<ref xml:lang="greek" target="([^"]+)">[^<]+</ref>[ ]+<ref>([^<]+)',line)):
      m= re.search(r'<ref xml:lang="greek" target="([^"]+)">[^<]+</ref>[ ]+<ref>([^<]+)',line)
      sys.stderr.write("complexref\t"+m.group(1)+"\t"+m.group(2)+'\t')
      fullkey = m.group(1) + '-' + m.group(2)
      if( fullkey in allids):
        line = re.sub(r'<ref xml:lang="greek" target="([^"]+)">([^<]+)</ref>[ ]+<ref>([^<]+)','<ref xml:lang="greek" target="'+fullkey+'"><foreign xml:lang="greek">\g<2></foreign> \g<3>',line,1)
        sys.stderr.write('refhit\n')
      else:
        line = re.sub(r'<ref xml:lang="greek" target="([^"]+)">([^<]+)</ref>[ ]+<ref>([^<]+)','<ref xml:lang="greek" target="'+fullkey+'"><foreign xml:lang="greek">\g<2></foreign> \g<3>',line,1)
        sys.stderr.write('reffail\t' + line)
 
     
    line = re.sub(r'(<ref [^>]+>)<ref xml:lang="greek"[^>]+>([^<]+)<\/ref>[ ]+','\g<1><foreign xml:lang="greek">\g<2></foreign> ',line)

    line = re.sub(r':<\/p>',',</p>',line)
    line = re.sub(r'<gloss>(In)<\/gloss>','\g<1>',line)

    
    line = re.sub(r'(<p>Hence,[ ]+)([A-Za-z][^\=<]+)([ ]+<bib|[ ]+<cit|<\/p>)','\g<1><gloss>\g<2></gloss>\g<3>',line)
    line = re.sub(r'(<p>)([A-Z][^\=<]+)[ ]+(<bib|<cit|\()','\g<1><gloss>\g<2></gloss> \g<3>',line)
    line = re.sub(r'(<p>)([A-Z][^\=<]+<pb[^>]+>[^\=<]+)[ ]+(<bib|<cit|\()','\g<1><gloss>\g<2></gloss> \g<3>',line)

    line = re.sub(r':<\/hi>','</hi>:',line)
    line = re.sub(r'(<p>)([A-Z][^<=:]+:)[ ]+','\g<1><gloss>\g<2></gloss> ',line)
    line = re.sub(r'(,[ ]+etc\.|:)(<\/gloss>|<\/term>)','\g<2>\g<1>',line)
    line = re.sub(r'(<gloss>)(Absol\.|Hence),[ ]+','<term>\g<2></term>, \g<1>',line)
    line = re.sub(r'<term>(adv\.|gen\.|genit\.),\s+([^<]+)<\/term>([: ]+)(<cit|<bib)','<term>\g<1></term>, <gloss>\g<2></gloss>\g<3>\g<4>',line)


    line = re.sub(r'(<\/foreign>,[ ]+|</ref>,[ ]+)([A-Za-z ,\.]+)[ ]+(<bib|<cit|\()','\g<1><gloss>\g<2></gloss>\g<3>',line)
    line = re.sub(r'(<\/foreign>,[ ]+)([A-Za-z ,\.]+<pb[^>]+>[A-Za-z ,\.]+)[ ]+(<bib|<cit)','\g<1><gloss>\g<2></gloss>\g<3>',line)
    line = re.sub(r'<p>([A-Z][a-zA-Z ,\.]+)</p>','<p><gloss>\g<1></gloss></p>',line)
    line = re.sub(r'<p>([A-Z][a-zA-Z ,\.]+<pb[^>]+>[a-zA-Z ,\.]+)</p>','<p><gloss>\g<1></gloss></p>',line)
    line = re.sub(r'<p>([A-Z][a-zA-Z ,\.\'()]+<hi[^>]+>[^<]+<\/hi>[a-zA-Z ,\.]*)(:|\(|</p>|<bibl|:<\/p>)','<p><gloss>\g<1></gloss>\g<2>',line)
    line = re.sub(r'<p>([A-Z][a-zA-Z ,\.\'()]+<hi[^>]+>[^<]+<\/hi>[^>]+<hi[^>]+>[^<]+</hi>[^<:]*)(:|\(|</p>|<bibl::<\/p>)','<p><gloss>\g<1></gloss>\g<2>',line)

    line = re.sub(r'<gloss>Hence</gloss>','Hence',line)
    line = re.sub(r'<term>([^<]+)<term>([^>]+)</term>([^<]+)</term>','\g<1>\g<2>\g<3>',line)
    line = re.sub(r'\((twice)','(<term>\g<1></term>',line)
    line = re.sub(r'(<\/bibl>[ ]+\()([a-zA-Z, ]+)\)','\g<1><gloss>\g<2></gloss>)',line)
    line = re.sub(r'(<\/bibl>[ ]+\()(here[ ,]app\.[, ]+|app\.[ ,]+)([a-zA-Z, ]+)\)','\g<1>\g<2><gloss>\g<3></gloss>)',line)
    line = re.sub(r'(With <term>[a-z]+|<term>Absol\.),[ ]+([a-z][a-zA-Z ,]+)(<\/term>)','\g<1>\g<3>, <gloss>\g<2></gloss>',line)
    line = re.sub(r'<gloss>Also</gloss>','Also',line)
    
  
    print(line,end='')
f.close()

sys.stderr.write('terms='+str(terms)+'\n')
