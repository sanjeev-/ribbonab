import abyes as ab
import numpy as np
import matplotlib.pyplot as plt

def create_array_data(sample_size, conversion_rate):
    zero_array = np.zeros(sample_size)
    total_ones = int(conversion_rate * sample_size)
    for idx in range(total_ones):
        zero_array[idx] = 1
    return zero_array

def lists_to_dictarray(list_x, list_y, color):
    line = []
    for idx, item in enumerate(list_x):
        line.append(
        {
            'x': item,
            'y': list_y[idx],
            'c': color, 
        }
        )
    return line

class BayesTest:
    def __init__(self, control_conv_rate, test_conv_rate, control_sample_size, test_sample_size, 
                 method = 'analytic', decision_var = 'lift', rule = 'rope', alpha = 0.95, rope = (-0.1, 0.1)):
        self.control_conv_rate = control_conv_rate
        self.test_conv_rate = test_conv_rate
        self.control_sample_size = control_sample_size
        self.test_sample_size = test_sample_size
        self.method = method
        self.decision_var = decision_var
        self.rule = rule
        self.alpha = alpha
        self.rope = rope
        
    def create_data(self):
        data_control = create_array_data(self.control_sample_size, self.control_conv_rate)
        data_test = create_array_data(self.test_sample_size, self.test_conv_rate)
        data = [data_control,data_test]
        return data
    
    def run_exp(self,data):
        exp = ab.AbExp(method=self.method, decision_var = self.decision_var, rule=self.rule, rope=(-0.01,0.01), alpha=self.alpha, plot=True)
        exp.experiment(data)
        
    def print_plot_rope_posterior(self,data):
        var='lift'
        exp = ab.AbExp(method=self.method, decision_var = self.decision_var, rule=self.rule, rope=(-0.01,0.01), alpha=self.alpha, plot=True)
        posterior = exp.find_posterior(data)
        bins = posterior['lift'][1]
        x = 0.5 * (bins[0:-1] + bins[1:])
        pdf = posterior['lift'][0]
        k = np.linspace(0, max(pdf), 1000)
        area_above = np.array([np.trapz(pdf[pdf >= kk], x[pdf >= kk]) for kk in k])
        index = np.argwhere(np.abs(area_above - self.alpha) == np.min(np.abs(area_above - self.alpha)))[0]
        label1 = r'$f(\mu_A)$'
        label2 = r'$f(\mu_B)$'
        label3 = 'HPD'
        label4 = 'ROPE'
        if var == 'es':
            label = '$f$(ES)'
        elif var == 'lift':
            label = r'$f(\mu_B - \mu_A)$'
        ls = '-'
        
        plt.subplot(1, 2, 1)
        b = posterior['muA'][1]
        line, = plt.plot(0.5 * (b[0:-1] + b[1:]), posterior['muA'][0], ls=ls, lw=2, label=label1)
        if 'clr' in locals():
            line.set_color(clr)
        b = posterior['muB'][1]
        line, = plt.plot(0.5 * (b[0:-1] + b[1:]), posterior['muB'][0], ls=ls, lw=2, label=label2)
        if 'clr' in locals():
            line.set_color(clr)
        plt.xlabel('$\mu_A,\  \mu_B$')
        plt.xlim([0, 1])
        plt.title('Conversion Rate')
        plt.gca().set_ylim(bottom=0)
        plt.locator_params(nticks=6)
        plt.legend()
        
        plt.subplot(1, 2, 2)
        pdf = posterior['lift'][0]
        line, = plt.plot(x, pdf, lw=3, ls='-', label=label)
        if 'clr' in locals():
            line.set_color(clr)
        plt.plot(x[pdf >= k[index]], 0 * x[pdf >= k[index]], linewidth=4, label=label3)
        plt.xlim([np.minimum(np.min(x), -1), np.maximum(1, np.max(x))])
        plt.plot([self.rope[0], self.rope[0]], [0, 4], 'g--', linewidth=5, label=label4)
        plt.plot([self.rope[1], self.rope[1]], [0, 4], 'g--', linewidth=5)
        plt.gca().set_ylim(bottom=0)
        plt.gca().locator_params(axis='x', numticks=6)
        plt.legend()
        if var == 'es':
            plt.xlabel(r'$(\mu_B-\mu_A)/\sqrt{\sigma_A^2 + \sigma_B^2)}$')
            plt.title('Effect Size')
        elif var == 'lift':
            plt.xlabel(r'$\mu_B-\mu_A$')
            plt.title(r'Lift')
        plt.savefig('testfig.png')
    
    def create_posteriors(self, data):
        var='lift'
        exp = ab.AbExp(method=self.method, decision_var = self.decision_var, rule=self.rule, rope=(-0.01,0.01), alpha=self.alpha, plot=True)
        posterior = exp.find_posterior(data)
        bins = posterior['lift'][1]
        x = 0.5 * (bins[0:-1] + bins[1:])
        pdf = posterior['lift'][0]
        k = np.linspace(0, max(pdf), 1000)
        area_above = np.array([np.trapz(pdf[pdf >= kk], x[pdf >= kk]) for kk in k])
        index = np.argwhere(np.abs(area_above - self.alpha) == np.min(np.abs(area_above - self.alpha)))[0]
        muA_line_b = posterior['muA'][1]
        muA_line  = 0.5 * (muA_line_b[0:-1] + muA_line_b[1:])
        muB_line_b = posterior['muB'][1]
        muB_line = 0.5 * (muB_line_b[0:-1] + muB_line_b[1:])
        
        pdf = posterior['lift'][0]
        
        line_x = x[pdf >= k[index]]
        line_y = 0 * x[pdf >= k[index]]
        
        x_lims = [np.minimum(np.min(x), -1), np.maximum(1, np.max(x))]
        
        json_dict = [
            {
                'label': 'posterior_control',
                'x': list(muA_line),
                'y': list(posterior['muA'][0]),
            },
            {
                'label': 'posterior_hypothesis',
                'x': list(muB_line),
                'y': list(posterior['muB'][0]),
            },
            {
                'label': 'lift_pdf',
                'x': list(x),
                'pdf': list(pdf)
            },

        ]

        posterior_control = lists_to_dictarray(list(muA_line),list(posterior['muA'][0]), 'red')
        posterior_hypothesis = lists_to_dictarray(list(muB_line), list(posterior['muB'][0]), 'green')
        lift_pdf = lists_to_dictarray(list(x), list(pdf), 'blue')

        d3dict = {
            'posterior_control': posterior_control,
            'posterior_hypothesis': posterior_hypothesis,
            'lift_pdf': lift_pdf
        }

        return d3dict
    
    def simple(self, data):
        var='lift'
        exp = ab.AbExp(method=self.method, decision_var = self.decision_var, rule=self.rule, rope=(-0.01,0.01), alpha=self.alpha, plot=True)
        posterior = exp.find_posterior(data)
        bins = posterior['lift'][1]
        x = 0.5 * (bins[0:-1] + bins[1:])
        pdf = posterior['lift'][0]
        k = np.linspace(0, max(pdf), 1000)
        area_above = np.array([np.trapz(pdf[pdf >= kk], x[pdf >= kk]) for kk in k])
        index = np.argwhere(np.abs(area_above - self.alpha) == np.min(np.abs(area_above - self.alpha)))[0]
        muA_line_b = posterior['muA'][1]
        muA_line  = 0.5 * (muA_line_b[0:-1] + muA_line_b[1:])
        muB_line_b = posterior['muB'][1]
        muB_line = 0.5 * (muB_line_b[0:-1] + muB_line_b[1:])
        
        pdf = posterior['lift'][0]
        
        line_x = x[pdf >= k[index]]
        line_y = 0 * x[pdf >= k[index]]
        
        x_lims = [np.minimum(np.min(x), -1), np.maximum(1, np.max(x))]
        x_lims = list(x_lims)
        x_lims = [str(x) for x in x_lims]
        
        graph_dict =[{
            'label': 'test series',
            'x':[0,1,2,3,4,5],
            'y':[5,10,20,30,50],
        }]
        
        return graph_dict

    def get_rope_decision(self, data, control, hypothesis):
        exp = ab.AbExp(method=self.method, decision_var = self.decision_var, rule=self.rule, rope=(-0.01,0.01), alpha=self.alpha, plot=True)
        posterior = exp.find_posterior(data)
        bins = posterior['lift'][1]
        x = 0.5 * (bins[0:-1] + bins[1:])
        pdf = posterior['lift'][0]
        k = np.linspace(0, max(pdf), 1000)
        area_above = np.array([np.trapz(pdf[pdf >= kk], x[pdf >= kk]) for kk in k])
        index = np.argwhere(np.abs(area_above - self.alpha) == np.min(np.abs(area_above - self.alpha)))[0]
        hpd_output = x[pdf >= k[index]]
        rope_decision = exp.rope_decision(hpd_output)
        decision = 'Something went wrong!'
        if np.isnan(rope_decision):
            decision = 'Experiment is inconclusive -- gather more data!'
        if rope_decision == -1:
            decision = 'Experiment is conclusive.  {} (Control) is statistically greater than  {} (Hypothesis)'.format(control, hypothesis)
        if rope_decision == 1:
            decision = 'Experiment is conclusive.  {} (Hypothesis) is statistically greater than {} (Control)'.format(hypothesis, control)
        return decision


