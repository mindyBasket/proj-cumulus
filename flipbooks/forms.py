from django.contrib import messages
from django import forms

from .models import (
    Frame,
    Strip,
    Scene
)

# .................................................. 
# .................................................. 
#                   Frame forms 
# .................................................. 
# .................................................. 

class FrameForm(forms.ModelForm):
    class Meta:
        model = Frame
        fields = ['note', 'order', 'frame_image', 'strip']


# .................................................. 
# .................................................. 
#                   Strip forms 
# .................................................. 
# .................................................. 

def string2List(stringyList):
    # assumes items are listed with "," only (for now)
    li = stringyList.split(",")
    
    #clean up
    return list( item.strip() for item in li )
    
def list2String(li):
    return ','.join(str(item) for item in li)

def getOrderChoices(scene_instance, curr_strip_id=-1):
    
    sc = scene_instance
    
    if not sc:
        return ()
    else:
        order_choices = [] # to be turned into final tuple
        last_order = 0 # last order if you want to put this strip last
        
        # get list of strip.id in order
        strip_in_order = string2List(sc.children_orders)
        print("---------retrieve children_orders: {} with length {}".format(strip_in_order, len(strip_in_order)))
        
        #validate list
        if len(strip_in_order) == 0 or (len(strip_in_order)==1 and strip_in_order[0]==''):
            return ((-1, "Error: Cannot find order reference"),)
        
        for i, strip_id in enumerate(strip_in_order):
            #make tuple
            if strip_id == curr_strip_id:
                #is current instance's order
                order_select = ((i+1), "{}(id#{}) - CURRENT".format(i+1,strip_id)) 
            else:
                order_select = ((i+1), "{}(id#{}) - taken".format(i+1,strip_id)) 
            order_choices.append(order_select)
            
            last_order=i+1
            
        #add new order
        new_order_select = (last_order+1, "+({} - new)".format(last_order+1)) 
        order_choices.append(new_order_select)
        
        #turn it into tuple
        return tuple(order_choices)
    

class StripCreateForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(StripCreateForm, self).__init__(*args, **kwargs)
        
        #order Scene by its 'order' attribute
        self.fields['scene'].queryset = Scene.objects.order_by("order")
        # self.fields['scene'] = forms.ModelChoiceField(
        #     queryset=Scene.objects.order_by("order")
        # )

    class Meta:
        model = Strip
        fields = ['scene', 'description'] #removed 'order'. No need to select them.
        # https://docs.djangoproject.com/en/1.10/topics/forms/modelforms/#overriding-the-default-fields
        labels = {
            'scene': 'Under scene'
        }
        
        #so I would like to add class to these fields. To do it, investigate crispy forms.
        
    #not part of ModelForm
    # def form_valid()



class StripUpdateForm(forms.ModelForm):
    
    # Originally integerfield. Now dynamically updated ChoiceField 
    order = forms.ChoiceField(choices=(), label="At order")
    
    def __init__(self, *args, **kwargs):
        strip_instance = kwargs['instance']
        strip_orders_list = []
        for strip in strip_instance.scene.strip_set.all():
            strip_orders_list.append(strip.order)
            
        super(StripUpdateForm, self).__init__(*args, **kwargs)
        
        self.fields['order'].choices = getOrderChoices(strip_instance.scene, curr_strip_id=strip_instance.id)
        
        
    class Meta:
        model = Strip
        fields = ['scene', 'order', 'description'] 
        labels = {
            'scene': 'Under scene',
            'order': 'Does not override' #it seems it cannot override when field changed in form class
        }
        # widgets = {
        #     # below seem to get treated as...not even a field with a value
        #     #'scene': forms.Select(attrs={'disabled': 'disabled'}),
        #     'order': forms.Select,
        # }

    # This also exists in ModelForm? Originally I assumed it is only for Models
    # The difference is that, here, "self" is the ModelForm.
    # def save(self):
    #     #add better order if it is set 0
    #     if int(self.order) == 0:
    #         self.order = get_last_order(self)
        
    #     super(Strip, self).save()