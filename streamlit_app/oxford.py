import streamlit as st
import re
import xml.etree.ElementTree as et

# Hàm tìm vị trí của từ trong từ điển
def findword(nhap_1_tu, root):
    kq = root.findall(".//runhd")
    for tu in kq:
        if tu.text == nhap_1_tu:
            print("word = ", tu.text)
            return tu
    return None

# Hàm tìm cha của 1 node
def findfather(ptu, root):
    parent = None
    for i in root.iter():  # Duyệt qua tất cả các node từ root xuống
        for child in i:
            if child == ptu:
                parent = i
                break
        if parent is not None:
            break
    return parent

# Functions for EEV Dictionary Processing
def textprocess(chuoi):
    newchuoi = chuoi.strip()
    kytudb = r'[=~!@#$%^&*<>?:{}|\\\[\]/]'
    newchuoi = re.sub(r'/[^/]+/', "", newchuoi)
    newchuoi = re.sub(kytudb, "", newchuoi)
    newchuoi = re.sub(r'\s{2,}', ' ', newchuoi)
    newchuoi = newchuoi.replace(" ,", ",")
    return newchuoi

def text_outside_children(nodecha):
  full_text = ''.join(nodecha.itertext())   # Get all text within the parent node
  #print("** full_text = ", full_text) ; 
  txt_v_s_srf=nodecha.find(".//txt_v_s_srf")
  txt_v_s_srf_texts=''.join(txt_v_s_srf.itertext()) ;  print ("txt_v_s_srf = ", txt_v_s_srf_texts) # chuỗi các text có dưới tag <txt_v_s_srf>
  full_text=full_text.replace(txt_v_s_srf_texts,"") ;# loại các text có trong <txt_v_s_srf>: text, tail, con-cháu
  
  symbol=nodecha.find(".//txt_v_s_srf")
  symbol_texts=''.join(symbol.itertext())  # chuỗi các text có dưới tag <symbol>
  full_text=full_text.replace(symbol_texts,"").replace("","")  # loại các text có trong <symbol>: text, tail, con-cháu
  #print("** full_text Sau khi loại nghĩa việt = ",full_text)  # loại tag nghĩa tiếng việt ra khỏi chuỗi
  # Remove text inside any child nodes
  for child in nodecha:
    if child.tag == nodecha.tag: continue  # bỏ qua nodecha không xét
    if child.tag == "dh": continue      # Thông in trong node <dh> là lấy, trong z là lấy, không có bỏ ra
    if child.tag == "z": continue
    #print("node con là = ", child.tag)
    child_text = ''.join(child.itertext()) ; print("** child_text = ", child_text.strip())
    if child_text ==" " : continue
    full_text = full_text.replace(child_text, '').replace("‘","").replace("’","")
    
  # Clean up and return the result
  return ' '.join(full_text.split()).strip()
    
def extract_example_text(node):
    """
    Extracts and processes example text from a given XML node.
    Handles nested elements like <gl>, <xr>, and <xh> correctly.
    """
    # Lấy văn bản bên trong phần tử <x>
    text_x = node.text.strip() if node.text else ''

    # Tìm phần tử <gl> và lấy toàn bộ nội dung
    gl_element = node.find('.//gl')

    # Xử lý phần tử <gl> nếu tồn tại
    if gl_element is not None:
        # Lấy toàn bộ nội dung của phần tử <gl>, bao gồm cả văn bản và thẻ XML
        text_gl = et.tostring(gl_element, encoding='unicode').strip()
        
        # Loại bỏ các thẻ XML trong toàn bộ nội dung của <gl> và xóa khoảng trắng dư thừa
        clean_text_gl = re.sub(r'<[^>]+>', '', text_gl).strip()
        
        # Xóa khoảng trắng thừa ở giữa các phần của câu
        clean_text_gl = re.sub(r'\s+', ' ', clean_text_gl).strip()
        
        # Kết hợp văn bản từ các phần tử
        result = f"{text_x} {clean_text_gl}"
    else:
        result = text_x

    # Xóa khoảng trắng thừa ở giữa các phần của câu
    result = re.sub(r'\s+', ' ', result).strip()

    return result
def meaningex(d_ud, root):
    """
    Hàm nhập vào 1 mảng 1 node <d> hay <ud>, trả về nghĩa tiếng Anh, tiếng Việt, và các ví dụ của 1 nghĩa của node <d> đó.
    """

    #print("@ Hàm meaningex(d_ud)")

    # Nghĩa tiếng Anh
    #print(" * Nghĩa tiếng Anh: ", end="")
    em = ""
    dhs = ""
    
    if d_ud.tag in ["d", "ud"]:
        em = text_outside_children(d_ud)
        print(em, end="")

        dhs_node = d_ud.find(".//dhs")
        if dhs_node is not None:
            dhs = "\'" + dhs_node.text + "\'"
            print(" dhs = ", dhs)
        
        for dud in d_ud.iter():
            if dud.tag not in ["d", "ud", "dhs", "txt_v_s_srf", 'symbol', "space", 'meaning', "z_xr", "i", "z", "xr", "xh", "cap_in_xh"]:
                text = dud.text if dud.text else ""
                tail = dud.tail if dud.tail else ""
                em += " " + text + tail

        em = em.strip() + " " + dhs
        print(" final em = ", em)
    
    elif d_ud.tag == "xr":
        for dud in d_ud.iter():
            text = dud.text.strip() if dud.text else ""
            tail = dud.tail.strip() if dud.tail else ""
            print(text, tail, " ", end="")
            em += text + tail

        em = em.strip()

    # Nghĩa tiếng Việt
    vm = ""
    print("")  # Để tắt end=""
    txt_v_s_srf = d_ud.find(".//txt_v_s_srf")

    if txt_v_s_srf is not None:
        #print("@ Nghĩa tiếng Việt: ", end="")
        for txt in txt_v_s_srf.iter():
            text = txt.text.strip() if txt.text else ""
            tail = txt.tail.strip() if txt.tail else ""
            vm += text + tail
            print(" vm= ", vm)
        
        vm = vm.strip()
        print(" vm 2= ", vm)
    
    # Các ví dụ
    print()  # Để tắt end=""
    vidu = findfather(d_ud).findall(".//x")
    print("vidu = ", vidu)
    
    ex = []  # Lưu tất cả các ví dụ của 1 nghĩa tiếng Anh

    for x in vidu:
        kq1 = ''.join(x.itertext())  # Nối tất cả các văn bản
        kq2 = ' '.join(kq1.split())  # Làm sạch văn bản
        ex.append(kq2)
        print("ex = ", ex)
    
    return em, vm, ex  # Trả về chuỗi định nghĩa tiếng Anh, định nghĩa tiếng Việt và mảng các ví dụ của 1 nghĩa của 1 loại từ của 1 từ

def thongtin1tu(word, root):
    thongtin = {
        'pronunciation': [],
        'word_type': [],
        'meanings': []
    }

    runhd = findword(word, root)
    if runhd is None:
        return thongtin

    father = findfather(runhd, root)
    grand = findfather(father, root)
    greatgrand = findfather(grand, root)

    phienam = father.findall(".//i")
    for j in phienam:
        thongtin['pronunciation'].append(j.text)

    p_g = greatgrand.findall(".//p-g")
    if not p_g:
        word_type = greatgrand.find(".//z_p")
        thongtin['word_type'].append(word_type.text.strip() if word_type is not None else "Không xác định")

        n_g = greatgrand.findall(".//n-g")
        if not n_g:
            d_ud = greatgrand.find(".//d") or greatgrand.find(".//ud") or greatgrand.find(".//xr")
            if d_ud:
                em, vm, ex = meaningex(d_ud, root)
                meaning_info = {
                    'meanings_english': em,
                    'meanings_vietnamese': vm,
                    'examples': ex,
                    'word_type': thongtin['word_type'][0]
                }
                thongtin['meanings'].append(meaning_info)
        else:
            for ng in n_g:
                if findfather(ng, root).tag not in ['pv-g', 'id-g']:
                    zn = ng.find(".//zn")
                    meaning_info = {
                        'meanings_english': zn.text.strip() if zn is not None else "Không xác định",
                        'meanings_vietnamese': None,
                        'examples': [],
                        'word_type': thongtin['word_type'][0]
                    }
                    d_ud = ng.find(".//d") or ng.find(".//ud") or ng.find(".//xr")
                    if d_ud:
                        em, vm, ex = meaningex(d_ud, root)
                        meaning_info['meanings_english'] = em
                        meaning_info['meanings_vietnamese'] = vm
                        meaning_info['examples'].extend(ex)
                    thongtin['meanings'].append(meaning_info)
    else:
        for pg in p_g:
            word_type = pg.find(".//z_p_in_p-g")
            current_word_type = word_type.text.strip() if word_type is not None else "Không xác định"
            thongtin['word_type'].append(current_word_type)

            n_g = pg.findall(".//n-g")
            if not n_g:
                d_ud = pg.find(".//d") or pg.find(".//ud") or pg.find(".//xr")
                if d_ud:
                    em, vm, ex = meaningex(d_ud, root)
                    meaning_info = {
                        'meanings_english': em,
                        'meanings_vietnamese': vm,
                        'examples': ex,
                        'word_type': current_word_type
                    }
                    thongtin['meanings'].append(meaning_info)
            else:
                for ng in n_g:
                    if findfather(ng, root).tag not in ['pv-g', 'id-g']:
                        zn = ng.find(".//zn")
                        meaning_info = {
                            'meanings_english': zn.text.strip() if zn is not None else "Không xác định",
                            'meanings_vietnamese': None,
                            'examples': [],
                            'word_type': current_word_type
                        }
                        d_ud = ng.find(".//d") or ng.find(".//ud") or ng.find(".//xr")
                        if d_ud:
                            em, vm, ex = meaningex(d_ud, root)
                            meaning_info['meanings_english'] = em
                            meaning_info['meanings_vietnamese'] = vm
                            meaning_info['examples'].extend(ex)
                        thongtin['meanings'].append(meaning_info)

    back_meanings = []
    for index, meaning in enumerate(thongtin['meanings'], start=1):
        meaning_info = {
            "Keyword": f"{index}",
            "Description": meaning['meanings_english'],
            "Meaning_Vietnamese": meaning['meanings_vietnamese'],
            "Examples": meaning['examples'],
            "Word_Type": meaning['word_type'],
            "Pronunciation": ", ".join(thongtin['pronunciation'])
        }
        back_meanings.append(meaning_info)

    return back_meanings
