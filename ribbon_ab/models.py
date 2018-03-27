from django.db import models

# Create your models here.

class BayesianABTest(models.Model):
    experiment_name = models.CharField(max_length=50)
    experiment_person = models.CharField(max_length = 50, default = 'sanjeev')
    experiment_type = models.CharField(max_length=50)
    control = models.CharField(max_length=50)
    hypothesis = models.CharField(max_length=50)
    control_sample_size = models.IntegerField(blank = True, null = True)
    hypothesis_sample_size = models.IntegerField(blank = True, null = True)
    control_conversion_rate = models.FloatField(blank = True, null = True)
    hypothesis_conversion_rate = models.FloatField(blank = True, null = True)
    analysis_type = models.CharField(max_length = 50, default = 'analytic')
    decision_variable = models.CharField(max_length = 50, default = 'lift')
    decision_rule = models.CharField(max_length = 50, default = 'rope')
    decision_alpha = models.FloatField(default = 0.95)
    slug = models.SlugField(max_length=40, default = 'test-slug')


