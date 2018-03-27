from django.shortcuts import render
from django.http import HttpResponse
from matplotlib import pylab
from pylab import *
import PIL
import PIL.Image
import io
from .analytics import *
import matplotlib
import json
from .models import BayesianABTest
from .forms import ABTestForm
from django.shortcuts import redirect



# Create your views here.

def about_view(request):

    context = {
    }
    return render(request,'about.html',context)

def dashboard_view(request):
    qs = BayesianABTest.objects.all()

    context = {
        'qs': qs
    }
    return render(request,'dashboard.html',context)

def experiment_view(request, experiment_slug):

    exp = BayesianABTest.objects.get(slug=experiment_slug)

    experiment_name = exp.experiment_name
    experiment_person = exp.experiment_person
    experiment_type = exp.experiment_type
    control = exp.control
    hypothesis = exp.hypothesis
    control_sample_size = exp.control_sample_size
    hypothesis_sample_size = exp.hypothesis_sample_size
    control_conversion_rate = exp.control_conversion_rate
    control_perc = round(control_conversion_rate * 100, 2)
    hypothesis_conversion_rate = exp.hypothesis_conversion_rate
    hypothesis_perc = round(hypothesis_conversion_rate * 100, 2)
    analysis_type = exp.analysis_type
    decision_variable = exp.decision_variable
    decision_rule = exp.decision_rule
    decision_alpha = exp.decision_alpha
    slug = exp.slug
    rope_lower = round(control_perc * 0.9, 2)
    rope_upper = round(control_perc * 1.1, 2)

    AB = BayesTest(control_conversion_rate, hypothesis_conversion_rate, control_sample_size, hypothesis_sample_size)
    data = AB.create_data()
    posterior_data = AB.create_posteriors(data)
    print(posterior_data)
    ab_json = json.dumps(posterior_data, indent = 4, ensure_ascii=False)

    rope_decision = AB.get_rope_decision(data, control, hypothesis)

    context = {
        'experiment_name': experiment_name,
        'experiment_person': experiment_person, 
        'experiment_type': experiment_type, 
        'control': control,
        'hypothesis': hypothesis, 
        'control_sample_size': control_sample_size,
        'hypothesis_sample_size': hypothesis_sample_size,
        'control_conversion_rate': control_conversion_rate,
        'hypothesis_conversion_rate': hypothesis_conversion_rate,
        'analysis_type': analysis_type,
        'decision_variable': decision_variable,
        'decision_rule': decision_rule,
        'decision_alpha': decision_alpha,
        'ab_json': ab_json,
        'rope_decision': rope_decision,
        'control_perc': control_perc,
        'hypothesis_perc': hypothesis_perc,
        'rope_lower': rope_lower,
        'rope_upper': rope_upper,
    }

    return render(request, 'experiment.html', context)

def bayes_view(request):
    context = {}
    ab = BayesTest(0.4,0.5,3000,3000)
    data = ab.create_data()
    ab_dict = ab.create_posteriors(data)
    d = json.dumps(ab_dict)
    context['d'] = d
    print(d)
    return render(request,'dashboard.html',context)

def experiment_new(request):
    if request.method == "POST":
        form = ABTestForm(request.POST)
        if form.is_valid():
            abtest = form.save(commit=False)
            abtest.save()
            return redirect('/dashboard')
    else:
        form = ABTestForm()
    return render(request,'new_experiment.html',{'form': form})
