from django import forms
from .models import BayesianABTest

class ABTestForm(forms.ModelForm):


    class Meta:
        model = BayesianABTest
        fields = ('experiment_name', 'experiment_person', 'experiment_type', 'control', 'hypothesis', 
                    'control_sample_size', 'hypothesis_sample_size', 'control_conversion_rate', 'hypothesis_conversion_rate',
                    'slug')