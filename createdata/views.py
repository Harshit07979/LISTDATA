from xml.dom.minidom import Element
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest, HttpResponse
import logging
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import pandas as pd
import io
from django.contrib import messages


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# List Functions
def create_list():
    return [1, 2, 3]

def add_to_list(lst, element):
    lst.append(int(element))
    logging.info(f'Added {element} to list, resulting list: {lst}')
    return lst

def remove_from_list(lst, element):
    element = int(element)
    if element in lst:
        lst.remove(element)
        logging.info(f'Removed {element} from list, resulting list: {lst}')
    else:
        logging.error(f'Element {element} not found in list')
        raise ValueError("Element not found in list")
    return lst

def modify_list(lst, index, new_element):
    index = int(index)
    new_element = int(new_element)
    if 0 <= index < len(lst):
        old_element = lst[index]
        lst[index] = new_element
        logging.info(f'Modified index {index} from {old_element} to {new_element}, resulting list: {lst}')
    else:
        logging.error(f'Index {index} out of range')
        raise IndexError("Index out of range")
    return lst


# Dictionary Functions
def create_dict():
    return {'a': 1, 'b': 2, 'c': 3}

def add_to_dict(dct, key, value):
    dct[key] = int(value)
    logging.info(f'Added key {key} with value {value} to dictionary, resulting dictionary: {dct}')
    return dct

def remove_from_dict(dct, key):
    if key in dct:
        del dct[key]
        logging.info(f'Removed key {key} from dictionary, resulting dictionary: {dct}')
    else:
        logging.error(f'Key {key} not found in dictionary')
        raise KeyError("Key not found in dictionary")
    return dct

def modify_dict(dct, key, new_value):
    if key in dct:
        old_value = dct[key]
        dct[key] = int(new_value)
        logging.info(f'Modified key {key} from {old_value} to {new_value}, resulting dictionary: {dct}')
    else:
        logging.error(f'Key {key} not found in dictionary')
        raise KeyError("Key not found in dictionary")
    return dct


# Set Functions
def create_set():
    return {1, 2, 3}

def add_to_set(st, element):
    st.add(int(element))
    logging.info(f'Added {element} to set, resulting set: {st}')
    return st

def remove_from_set(st, element):
    element = int(element)
    if element in st:
        st.remove(element)
        logging.info(f'Removed {element} from set, resulting set: {st}')
    else:
        logging.error(f'Element {element} not found in set')
        raise KeyError("Element not found in set")
    return st

def check_in_set(st, element):
    exists = int(element)in st
    logging.info(f'Checked if {element} is in set: {exists}')
    return exists

### VIEWS
def index(request):
    print("Rendering index view")
    return render(request,'createdata/index.html')

def list_operations(request):
    lst = request.session.get('list', create_list()) 
    if request.method == 'POST':
        action = request.POST.get('action')
        element = request.POST.get('element')
        index = request.POST.get('index')
        new_element = request.POST.get('new_element')

        if action == 'add':
            lst = add_to_list(lst, element)
            # request.session['list'] = lst
            # messages.success(request, f'Added {element} to list.')
        elif action == 'remove':
            try:
                lst = remove_from_list(lst, element)
                # request.session['list'] = lst
                # messages.success(request, f'Removed {element} from list.')
            except ValueError as e:
                return HttpResponseBadRequest(str(e))
        elif action == 'modify':
            try:
                lst = modify_list(lst, int(index), new_element)
                # request.session['list'] = lst
                # messages.success(request, f'Modified index {index} in list.')
            except IndexError as e:
                return HttpResponseBadRequest(str(e))
        request.session['list'] = lst
            
    return render(request, 'createdata/list.html', {'list': lst})

# dictionary operation renderinh

def dict_operations(request):
    dct = request.session.get('dict', create_dict())
    if request.method == 'POST':
        action = request.POST.get('action')
        key = request.POST.get('key')
        value = request.POST.get('value')
        new_value = request.POST.get('new_value')

        if action == 'add':
            dct = add_to_dict(dct, key, value)
            # request.session['dict'] = dct
            # messages.success(request, f'Added key {key} with value {value} to dictionary.')
        
        elif action == 'remove':
            try:
                dct = remove_from_dict(dct, key)
                # request.session['dict'] = dct
                # messages.success(request, f'Removed key {key} from dictionary.')
            except KeyError as e:
                return HttpResponseBadRequest(str(e))
        elif action == 'modify':
            try:
                dct = modify_dict(dct, key, new_value)
                # request.session['dict'] = dct
                # messages.success(request, f'Modified value of key {key} in dictionary.')
            except KeyError as e:
                return HttpResponseBadRequest(str(e))
        request.session['dict'] = dct    
            
    return render(request, 'createdata/dict.html', {'dict': dct})

#set operation rendering
def set_operations(request):
    st = set(request.session.get('set', list(create_set())))
    if request.method == 'POST':
        action = request.POST.get('action')
        element = request.POST.get('element')
        
        if action == 'add':
            st = add_to_set(st, element)
            # request.session['set'] = st
            # messages.success(request, f'Added {element} to set.')
        elif action == 'remove':
            try:
                st = remove_from_set(st, element)
                # request.session['set'] = st 
                # messages.success(request, f'Removed {element} from set.')
            except KeyError as e:
                return HttpResponseBadRequest(str(e))
        elif action == 'check':
            exists = check_in_set(st, element)
            request.session['set'] = list(st)
            return render(request, 'createdata/set.html', {'set': st, 'exists': exists})
        request.session['set'] = list(st)
        
    return render(request, 'createdata/set.html', {'set': st})

def export_pdf(request):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.drawString(100, 750, "Data Structure Final States")
    
    lst = request.session.get('list', create_list())
    dct = request.session.get('dict', create_dict())
    st = set(request.session.get('set', list(create_set()))
)
    y = 700
    p.drawString(100, y, f"List: {lst}")
    y -= 30
    p.drawString(100, y, f"Dictionary: {dct}")
    y -= 30
    p.drawString(100, y, f"Set: {st}")

    p.showPage()
    p.save()

    buffer.seek(0)
    request.session.flush()


    return HttpResponse(buffer, content_type='application/pdf')

def export_excel(request):
    lst = request.session.get('list', create_list())
    dct = request.session.get('dict', create_dict())
    st = set(request.session.get('set', list(create_set())))

    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df_list = pd.DataFrame(lst, columns=["List"])
        df_dict = pd.DataFrame(list(dct.items()), columns=["Key", "Value"])
        df_set = pd.DataFrame(list(st), columns=["Set"])

        df_list.to_excel(writer, sheet_name='List', index=False)
        df_dict.to_excel(writer, sheet_name='Dictionary', index=False)
        df_set.to_excel(writer, sheet_name='Set', index=False)
    
    

    buffer.seek(0)
    request.session.flush()

    return HttpResponse(buffer, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')