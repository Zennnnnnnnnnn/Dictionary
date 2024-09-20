# Hàm tìm vị trí của từ trong từ điển: là tìm tag <runhd> chứa từ này
def findword(nhap_1_tu, root):
  kq = root.findall(".//runhd") ;
  for tu in kq:
    if tu.text == nhap_1_tu:
      print ("word = <" ,tu.tag,">","---------------",tu.text, "---------------")
      break
  return tu

# hàm tìm cha của 1 node: đầu vào là 1 node (tag) đầu ra sẽ trả về node cha
def findfather(ptu, root):
  papa=None
  for i in root.iter():   # root.iter() là toàn các nốt đi từ nốt root xuống
    if ptu in i: papa=i; break
  return papa

def textprocess (chuoi):   # hàm xử lý 1 chuỗi, loại bỏ các ký tự đặc biệt như /chuỗi nằm giữa 2 dấu này/ : ?  <nhiều khoảng trắng thừa"
  newchuoi=chuoi.strip()
  kytudb = r'[~@#$%^&*<>?:{}|\\\[\]]'           # không có dấu =, !, / ; r'[^\w\s]' với là tìm các ký tự không phải chữ cái hoặc khoảng trắng
  newchuoi= re.sub(r'/[^/]+/'," ", newchuoi)    # thay thế text nằm trong 2 dấu /..../ bằng khoảng trắng
  newchuoi= re.sub(kytudb," ",newchuoi)         # thay thế tất cả các ký tự đặc biệt thuộc kytudb bằng ""
  newchuoi= re.sub(r'\s{2,}', " ", newchuoi)    # Thay thế 2 khoảng trắng liên tiếp bằng 1 khoảng trắng
  newchuoi=newchuoi.replace(" ," , ",")         # nếu trước dấu phẩy có khoảng trắng thì bỏ đi
  newchuoi=newchuoi.replace(" , " , ", ")       # nếu trước dấu phẩy có khoảng trắng thì bỏ đi
  newchuoi=newchuoi.replace(" .",".")           # nếu trước dấu chấm có khoảng trắng thì bỏ đi
  newchuoi=newchuoi.replace(" . ",". ")         # nếu trước dấu chấm có khoảng trắng thì bỏ đi
  return newchuoi

#print("chuỗi đã lọc = ", textprocess("Mưa      : ? < > [ ],{ } \ | Rơi Rơi / abcde fgtg /"))


# hàm mới tạo 9pm 14-09-2024
# Hàm in ra các chuỗi nằm dưới 1 node (các chuỗi này nằm ngoài và trong tất cả các node con, cháu... của node)
def alltext_under1node(element):
    # Tạo một danh sách để chứa các chuỗi văn bản
    text_list = []
    # Duyệt qua tất cả các phần tử trong cây XML
    for elem in element.iter():
        # Nếu phần tử có văn bản, thêm vào danh sách
        if elem.text is not None:  # lưu ý đk này khác với đk "if elem.text:"
            text_list.append(elem.text.strip())
        # Nếu phần tử có văn bản đuôi (sau các phần tử con), thêm vào danh sách
        if elem.tail is not None:   # lưu ý đk này khác với đk "if elem.tail:"
            text_list.append(elem.tail.strip())

    # Kết hợp các chuỗi lại với nhau
    result = ' '.join(text_list)
    return result

# hàm lọc ra các text định nghĩa tiếng anh: nằm dưới node cha <d> hay <ud> nhưng không thuộc node con <symbol> và <txt_v_s_srf>
# <dh> chứa định 1 phần định nghĩa tiếng anh, còn <dhs> chứa 1 phần định nghĩa tiếng anh nằm trong 2 dấu nháy ' ...'
def text_outside_children(nodecha):  # node cha là node <d> hay <ud>
  #print(" --> vào hàm text_outside_children")
  full_text = ''.join(nodecha.itertext())   # lấy tất cả các chuỗi nằm dưới node cha, vậy gồm cả symbol và tiếng việt
  #print("** full_text under <d> = ", full_text) ;

  symbol=nodecha.find(".//symbol")
  if symbol is not None:  # nếu có tồn tại tag <symbol>, lưu ý đk này khác với đk "if symbol:"
    symbol_texts=''.join(symbol.itertext())  # chuỗi các text có dưới tag <symbol>
    full_text=full_text.replace(symbol_texts,"").replace("","")  # loại các text có trong <symbol>: text, tail, con-cháu

  txt_v_s_srf=nodecha.find(".//txt_v_s_srf"); #print("tìm được node txt_v_s_srf dưới node <d>", txt_v_s_srf)
  #z=findfather(nodecha).find("//.z")                      # VD từ beg, node <d> ngang cấp node <z>, vậy để từ <d> tìm được <z> thì phải lên nút cha của <d>
  #z = nodecha.find(".//z")  # xử lý cho từ beg, định nghĩa tiếng việt nằm ở node <z> van nài, cầu khẩn: </z>
  if txt_v_s_srf is not None: # lưu ý đk này khác với đk "if symbol:" : Nếu txt_v_s_srf là một giá trị "truthy", tức là giá trị không phải là None, False, 0, chuỗi rỗng '', danh sách rỗng [], từ điển rỗng {}, hoặc các cấu trúc dữ liệu khác mà Python coi là "falsy", thì điều kiện sẽ được coi là đúng.
    # nếu có tồn tại tag <txt_v_s_srf>, VD từ beg không có tag txt_v_s_srf, nghĩa việt nằm trong tag <z>
    #print("có tồn tại node txt_v_s_srf dưới node <d>")
    txt_v_s_srf_texts=''.join(txt_v_s_srf.itertext()) ; #print("các chuổi nằm dưới node txt_v_s_srf = ", txt_v_s_srf_texts) # các chuỗi nằm dưới tag <txt_v_s_srf>
    full_text=full_text.replace(txt_v_s_srf_texts,"")  ; #print(" full_text khi loai tieng viet = ", full_text) # loại các text có trong <txt_v_s_srf>: text, tail, con-cháu

  #elif z: # nếu không có tag <txt_v_s_srf>, nghĩa việt nằm trong tag <z>
   # z_texts = ''.join(z.itertext())  # chuỗi các text nằm dưới tag <z> như từ beg
   # full_text=full_text.replace(z_texts,"")

  # Clean up and return the result
  #print(" full_text nghia tieng anh cuoi cung = ", full_text)
  #print(" -->/// ra hàm text_outside_children")
  return ' '.join(full_text.split()).strip()

"""
print("---------   Kiểm tra kết quả hàm dictionary_1word(root,word) ---------")
file_paths = ["/B.xml"] # ["/A.xml", "/B.xml", "/C.xml"]
root, word_list = wordlist(file_paths)  # hàm trả về root và danh sách các từ trong file

List1="back"  # ankylosaur, ankh, ABM, apple, back, cat, bank
runhd=findword(root, List1 ); print("rundhd = ", runhd.text)
ong=findfather(findfather(runhd))
d=ong.find(".//d"); print (" tag d = ", d.tag)
print("text_outside_children = ", text_outside_children(d))
"""

def meaningex(d_ud, root):  # hàm nhập vào 1 mảng 1 node <d> hay <ud>, trả về nghĩa anh, việt, các ví dụ của 1 nghĩa của node <d> đó, là 1 nghĩa của 1 phân loại của 1 từ
  # các <d> và <ud> này phải nằm trong các tag <n-g>, mỗi tag <n-g> là 1 nghĩa, còn nằm trong tag <id-g> là các tag idiom
  # mảng các node <d> hay <ud> là node bắt đầu định nghĩa tiếng anh và tiếng việt của 1 nghĩa của 1 loại từ của 1 từ
  # nghĩa tiếng Anh: là vào tag <d> hay <ud> vét hết các text và ndung các node con và cháu (con <xr>--> cháu <xh>) có thể có, ngoại trừ 2 node <synbol> và <txt_v_s_srf>
  # baby buggy: từ này chỉ có noun, có 2 nghĩa, và không có <d> mà lại có <xr> --> <xh>
  #print(" --> vào Hàm meaningex(d_ud)")

  print(" + Nghĩa tiếng anh : ", end="") # text nằm trong d_ud và nằm ngoài các node con
  em = ""
  dhs=""
  if d_ud.tag in ["d", "ud"]:
    em = text_outside_children(d_ud) ;  #print(" em1 = ", em) # ------------ lưu nghĩa tiếng anh lại
    if "" in em: em = em[0:em.find("")]  #;  print(" em2 = ", em)  # VD từ beg, nếu em có chứa ký tự , thì bỏ đi chuỗi từ  trở đi, vì đây là đn tiếng việt
    #for dud in d_ud.iter():  # duyệt tất cả các node con-cháu-chắt của d_ud gồm <d>, <ud>, <xr> (trong <xr> có <xh>)
      #if dud.tag not in ["d","ud", "dh", "dhs", "txt_v_s_srf",'symbol', "space" , 'meaning',"z_xr","i","z", "xr", "xh", "cap_in_xh"]  :  # <symbol> --> <space> là ký hiệu ?,  <meaning> là của nghĩa tiếng Việt
      #  text= dud.text if dud.text else ""      ;
      #  tail= dud.tail if dud.tail else ""      ;
      #  em = em +  "" + text + tail  ;   # ----------  dùng để lưu nghĩa tiếng Anh lại
      #  print("em3 = ", em)
  elif d_ud.tag in ["xr"]:
    for dud in d_ud.iter():
      text= dud.text.strip() if dud.text else ""
      tail= dud.tail.strip() if dud.tail else ""
      print(text, tail, " ", end="")
      em = em + text + tail  # --------------  dùng để lưu nghĩa tiếng Anh lại
    em=em.strip();
  print(" + nghĩa tiếng anh trong hàm meaningex = ",em) # in nghĩa tiếng anh

  # nghĩa tiếng Việt
  vm="";
  print("") ;  # để tắt end=""
  txt_v_s_srf = d_ud.find(".//txt_v_s_srf");  # print("Có tag txt_v_s_srf ? = ", txt_v_s_srf)  # nghĩa tiếng việt lấy từ tag <txt_v_s_srf>
  list_z = findfather(d_ud, root).findall(".//z");  #print ("có tag z ? = ", list_z) # tìm các tag <z>, có lưu nghĩa tiếng Việt như từ beg
  if txt_v_s_srf is not None:  # nếu có nghĩa tiếng Việt, if txt_v_s_srf: điều kiện này sẽ khác. VD từ "B2B" chỉ có 1 loại từ là abbr., nghĩa Anh nằm trong node <xh> là cháu của <d>,không có nghĩa Việt xxxxxxxxxxxxxxxx
    print(" + Nghĩa tiếng Việt: ",end="")
    for txt in txt_v_s_srf.iter():  # xét các node từ node này cho tới các node con cháu ... của nó để lấy các text ra
      text= txt.text.strip() if txt.text else ""
      tail= txt.tail.strip() if txt.tail else ""
      vm = vm + text + tail ; # print ("vm= ", vm) # dùng để lưu nghĩa tiếng Việt lại

  elif "" in d_ud.text: # xet truong hop tu beg, trong tag <d> có nghĩa tiếng việt luôn "if sth is going begging, it is available because nobody else wants it bị ế"
    stt = d_ud.text.find("") ; #print("stt = ", stt) # tìm vị trí ký tự  trong text của node <d>
    vm = vm + d_ud.text[stt:] # lấy chuỗi từ vị trí ký hiệu  cho tới hết chuỗi định nghĩa tiếng anh
    #print("@@@ Nội dung text trong tag <z> = ", vm)
    # thứ tự xét "" in d_ud.text phải trước, rồi mới tới list_z is not None, vì tag <z> hầu như luôn có tồn tại nhưng có thể không chứa 
  if vm.endswith(':'):
    vm = vm[:-1]
  print ("vm= ", vm)
  """
  elif list_z is not None: # nếu không có tag <txt_v_s_srf> và có tag <z> như từ beg, mà nằm trong tag <z> van nài, cầu khẩn: </z>
    #print("@@@ Không tồn tại tag <txt_v_s_srf>,  có tồn tại tag <z>","z.tag = ")
    # vm = "".join(z.intertext())  # lấy tất cả các chuỗi nằm dưới tag <z>
    for z in list_z: # có thể có nhiều tag z, nhưng tag z nào mà nội dung text bắt đầu là  "" mới là định nghĩa tiếng việt
      z_text = z.text.strip(); # print("z.text = ", z_text)  # phai co strip để cắt khoảng trắng trước , vì có thể có hoặc không có khoảng trắng
      if z_text.startswith(""): vm = vm + z_text.replace("","").replace(":","") ; break  # thoát khỏi vòng lặp for
    vm=vm.strip(); print ("vm = ", vm)
  """

  # Các Ví dụ
  # Một tag <x> có thể có con chứa text là <cl_in_x>, <gl>, cháu chứa text là <xr>, chắt chứa text là <xh>, 1 cặp tag <x> là 1 VD
  print() # để tắt end=""
  vidu=findfather(d_ud, root).findall(".//x"); #print("vidu = ", vidu) # tìm tất cả các tag <x> của 1 nghĩa tiếng anh
  ex=[] # lưu tất cả các VD của 1 nghĩa tiếng anh, mỗi ptu của mảng ex chứa 1 VD
  for x in vidu:
    kq1=''.join(x.itertext()) # Nối tất cả các vb
    kq2=' '.join(kq1.split())  # làm sạch văn bản:tách bỏ các ký tự trắng như xuống dòng, tab, nối chúng lại bằng một khoảng trắng đơn
    ex.append(kq2 ) ;
  print(" + Ví dụ ex = ", ex)

  #print(" -->/// ra Hàm meaningex(d_ud)")

  return em, vm, ex # trả về chuỗi định nghĩa tiếng anh, đn tiếng việt và mảng các ví dụ của 1 nghĩa của 1 loại từ của 1 từ


# ---------------------------------------------------------------------------------------------

# tim tat ca cac tu trong tu dien EEV luu vao mang wordlist
#wordlist=[]
#for i in root.iter():   # Duyệt qua tất cả các node từ node root xuống các node con cháu của nó trong file xml
#    if i.tag == "runhd":  # tìm node có tên runhd
#      wordlist.append(i.text.strip())
#print("Số lượng từ có trong từ điển EEV: ",len(wordlist))

#wordlist= ["Advanced Higher"] # ["canary","ABM", "baby", "back", "baby buggy", "backsheesh", "baggy", "Aunt Sally","act", "after" ]
#for word in  wordlist [0000:20]:

def thongtin1tu(word, root): # hàm nhận đối số là 1 từ, trả về thông tin là 1 dictionary có các key là phiên âm và các từ loại, value của phiên âm là cách phiên âm, value của các loại từ là 1 mảng các phần tử dictionary, mỗi phần tử là 1 nghĩa của từ loại đó gồm đn anh, đn việt, các VD của từ
  #print("--> Vào Hàm dictionary_1word_xml(root,word)")
  thongtin = {} # tạo 1 biến dictionary rỗng, tên biến chính là từ word, chứa keys là phiên âm và các từ loại, values là phiên âm và định nghĩa, VD của từ word đầu vào
  runhd=findword( word,root) # tìm vị trí của từ trong từ điển: là tag <runhd> chứa từ đó
  father = findfather(runhd, root); #print("cha là = ", father.tag) # cha của word <top-g>
  grand = findfather(father,root); #print("ông là = ", grand.tag)  # ông của word là <h-g>
  greatgrand = findfather(grand, root); #print("xxx Ông cố là =", greatgrand.tag) #là <entry>
  result = []
  pronunciation=[]    # dùng để tạo 1 từ mới
  phienam=father.findall(".//i");
  for j in phienam:
    print("phiên âm = /", j.text,"/")
    pronunciation.append(j.text)

  thongtin["pronunciation"]=pronunciation  # ----------- Tạo 1 key "pronunciation" lưu phiên âm vào dictionary thongtin

  p_g=greatgrand.findall(".//p-g") ;  # print("Các tag <p-g>= ",p_g , end="") # Tìm các tag <p-g> chứa các loại từ;
  if not p_g : # nếu ds p_g rỗng, khong tim ra tag <p-g>, như từ backsheesh --> nếu chỉ có 1 loại từ duy nhất (không có tag <p-g>, mà chỉ có 1 tag <h-g>, lúc này <d> và <x> thuộc <h-g>)
    if greatgrand.find(".//z_p")is not None: ###############################3
      wordtype = greatgrand.find(".//z_p").text.strip()  # wordtype không có là không làm luôn, không được else
    else: return thongtin # như từ backsheesh là thoát luôn hàm return giá trị rỗng
    #wordtype = greatgrand.find(".//z_p").text.strip() if greatgrand.find(".//z_p") else "";  # Từ backsheesh: không có tag wordtype luôn #if greatgrand.find(".//z_p") else ""  ######################## wordtype ra rỗng
    #lấy print(" *** Có 1 loại từ duy nhất là - 1: ",wordtype)  # từ contemplative có 1 loại từ nhưng lại có tag <p-g> nên không vào đây mà vào TH bên dưới --> gây lỗi vì không có tag <z_p_in_p>
    thongtin[wordtype] =  [] # ---------- tạo 1 key có tên là chuỗi wordtype, key này là 1 mảng chứa các ptử dictionary, mỗi ptừ là 1 nghĩa
    n_g = greatgrand.findall(".//n-g") ; # print("dãy các tag <n-g>: ") # từ <entry> tìm các <n-g> chính là tag lưu số nghĩa của từ
    if not n_g : # nếu danh sách n_g rỗng (không dùng if n_g is None) nếu không có tag <n-g> --> Nếu chỉ có 1 nghĩa duy nhất
      #lấy print("   + Có 1 loại từ duy nhất là - 2: ", wordtype, " - Có 1 nghĩa duy nhất")
      if greatgrand.find(".//d") : d_ud = greatgrand.find(".//d") ; # dhs = greatgrand.find(".//dhs") ;   #<dhs> như AH, ABM
      elif greatgrand.find(".//ud") : d_ud = greatgrand.find(".//ud"); #dhs = greatgrand.find(".//dhs") ;#<dhs> chứa 1 phần định nghĩa là đặt trong ' ...'
      elif greatgrand.find(".//xr") : d_ud = greatgrand.find(".//xr") ;
      elif greatgrand.find(".//h-g") : d_ud = greatgrand.find(".//h-g") ; # xử lý từ này: barbarity
      if d_ud :  #chú ý từ barbarity
        em, vm, ex = meaningex(d_ud, root)  #d_ud là mảng chứa các <d> hoặc <ud>
        thongtin[wordtype].append({"em":em, "vm":vm, "ex":ex}) # ------------ chèn em, vm, ex vào thongtin, em: nghĩa tiếng anh, vm: nghĩa tiếng việt, ex: các ví dụ tiếng anh
    else: # nếu tồn tại các tag <n-g> --> có nhiều nghĩa (có tag <n-g> --> <zn>), tag <n-g> cũng có trong <id-g> và <pv-g>
      #lấy print("có 1 loại từ duy nhất là - 3 : ",wordtype, " - Có nhiều nghĩa") # chú ý từ BEG, APPLE  #####################################
      for ng  in n_g:  # xét từng nghĩa, vì mỗi <n-g> sẽ chứa 1 <zn> và 1 <d>
        #print("có tag : ", ng.tag) #  xxxxxxxxxxx test
        if findfather(ng).tag not in ['pv-g','id-g']: # vì <n-g> cũng có trong <pv-g> và <id-g>
          zn=ng.find(".//zn") # Tìm <zn>          # từ Aunt Sally có lỗi ở nghĩa thứ <zn>2 là không nằm trong <n_g>, còn <n_g> thứ 2 lại rỗng
          #Lấy print(f"* Nghĩa thứ :  {zn.text.strip()} " if zn is not None else "")      # Tìm các nghĩa 1, 2 ,3 ... của loại-từ này, tag <zn>, có 1 nghĩa thì kg có tag này, Aunt Sally có lỗi là <n_g> thứ 2 rỗng
          d_ud= ng.find(".//d");
          if ng.find(".//d") :    d_ud = ng.find(".//d"); #print ("tìm thấy <d>")
          elif ng.find(".//ud") : d_ud = ng.find(".//ud"); #print ("tìm thấy <ud>")
          elif ng.find(".//xr") : d_ud = ng.find(".//xr");  #print ("tìm thấy <xr>")
          if d_ud:
            em, vm, ex = meaningex(d_ud, root)  ;
            thongtin[wordtype].append({"em":em, "vm":vm, "ex":ex}) # --------- chèn em, vm, ex vào từ điển thongtin
        d_ud=None   # reset lại giá trị d_ud mỗi khi chạy vòng lặp for tiếp tục
  else: # nếu ds p_g không rỗng --> nếu có từ 2 loại từ trở lên--> có tag <p-g>, lúc này <d> và <x> thuộc <p-g>
    #lấy print("*** Có 2 loại từ trở lên: ")
    for pg in p_g: # xét từng loại từ
      z_p_in_p_g = pg.find(".//z_p_in_p-g") ; #print("*** Loại từ là: ", z_p_in_p_g.text.strip())
      if z_p_in_p_g is not None: ###############################33
        wordtype = z_p_in_p_g.text.strip()
      else: return thongtin  # nếu từ đó có 2 loại từ trở lên mà lại không có tag loại từ <z_p_in_p-g> thì thoát hàm luôn
      # wordtype = z_p_in_p_g.text.strip() if z_p_in_p_g else ""; # wordtype không có là không làm luôn chứ else là sai
      thongtin[wordtype] =  []    # ----------- tạo 1 key có tên là chuỗi wordtype, key này là 1 mảng chứa các ptử dictionary, mỗi ptừ là 1 nghĩa
      n_g = pg.findall(".//n-g")  # từ <p-g> tìm các <n-g> chính là số nghĩa của từ trong mỗi loại-từ
      if not n_g : # nếu ds n_g rỗng, nếu loại từ này chỉ có 1 nghĩa thì không có tag <n-g>
        #lấy print("Có nhiều loại từ, mà loại từ này Có 1 nghĩa duy nhất")
        if pg.find(".//d") : d_ud = pg.find(".//d");
        elif pg.find(".//ud") : d_ud = pg.find(".//ud");
        elif pg.find(".//xr") : d_ud = pg.find(".//xr") # hiện tại d_ud từ sau mà rỗng thì nó lấy giá trị của từ trước
        if d_ud: em, vm,ex = meaningex(d_ud, root) ; thongtin[wordtype].append({"em":em, "vm":vm, "ex": ex})   #----------- chèn em, vm, ex vào thongtin, d_ud là mảng chứa các <d> hoặc chỉ chứa các <ud>
      else:   # nếu ds n_g không rỗng --> nếu loại từ này có từ 2 nghĩa trở lên --> có nhiều tag n-g --> <zn>
        #lấy print("Có 2 loại từ trở lên, Có 2 nghĩa trở lên")
        for ng in n_g:  # xét từng nghĩa, vì mỗi <n-g> sẽ chứa 1 <zn>
          if findfather(ng, root).tag not in ['pv-g','id-g']:  # vì <n-g> cũng có trong <pv-g> và <id-g>
            zn=ng.find(".//zn") # Tìm <zn>
            #lấy print("* Nghĩa thứ : ",zn.text.strip() )
            if ng.find(".//d") : d_ud = ng.find(".//d");
            elif ng.find(".//ud") : d_ud = ng.find(".//ud");
            elif ng.find(".//xr") : d_ud = ng.find(".//xr")
            if d_ud: em, vm, ex = meaningex(d_ud, root); thongtin[wordtype].append({"em":em, "vm":vm, "ex":ex});   #xxxxxxxxxx chèn em, vm, ex vào thongtin
          d_ud=None

  #return thongtin  # thongtin là 1 đối tượng kiểu dictionary key là phiên âm pronunciation và từ loại wordtype:noun, verb, adj., adv., values của các keys này là nghĩa anh em, nghĩa việt, VD ex
# Convert thongtin to the desired output format
    for wordtype, meanings in thongtin.items():
        if wordtype == "pronunciation":
            continue  # Skip the pronunciation key
        
        for idx, meaning in enumerate(meanings):
            result.append({
                'Keyword': str(len(result) + 1),
                'Description': meaning['em'],
                'Meaning_Vietnamese': meaning['vm'],
                'Examples': meaning['ex'],
                'Word_Type': wordtype,
                'Pronunciation': pronunciation[0] if pronunciation else ''
            })

    return result  # Return the final list of dictionaries
