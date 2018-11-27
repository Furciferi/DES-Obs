# Author: Reese Wilkinson
# Email: rw264@sussex.ac.uk
# Last Update: 2018-11-26

# This code has been written during observation time, and may contain errors/be inefficient.
# Please update to your hearts content if you wish to.



import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import datetime
import os
import sys
import warnings
import argparse


def get_date():
	now = datetime.datetime.now()
	return now.year,now.month,now.day

def plot_each_filter_time(content,year,month,day,args):
	exp={}
	for itter in range(0,len(content)):
		line = content[itter].split()
		exp[line[0]]=line[1:]


	headers = ["ra","dec","ut","filter","exposure_time","secz","psf","sky","cloud","t_eff"]
	filters = ['u','g','r','i','z','Y']
	colours = ['k','g','r','m','pink','y']
	for band in filters:
		y=[]
		x = exp.keys()
		xvals=[]
		times=[]
		for item in x:
			temp=float(exp[item][headers.index("psf")])
			if exp[item][headers.index("filter")]!=band:
				continue

			xvals.append(item)
			temp_time=exp[item][headers.index("ut")].split(":")
			time_object = datetime.datetime(year,month,day,int(temp_time[0]),int(temp_time[1]),0)
			times.append(time_object)
			y.append(temp)
		median = np.median(y)
		fig,ax = plt.subplots()
		ax.scatter(times,y,marker="*",label="{} psf".format(band))
		ax.plot(times,[median]*len(times),label= "{} psf median: {}".format(band,round(median),c='k'))
		#ax.gcf().autofmt_xdate()
		plt.xlim(min(times),max(times))
		ax.set_xticklabels(times,rotation=90)
		ax.xaxis.set_major_formatter(dates.DateFormatter('%H:%M'))
		#print str(median)+ "in band {}".format(band)
		plt.legend()
		plt.tight_layout()
		plt.savefig("{}-band_psf.png".format(band))


def plot_each_filter_exp(content,year,month,day,args):
	exp={}
	for itter in range(0,len(content)):
		line = content[itter].split()
		exp[line[0]]=line[1:]


	headers = ["ra","dec","ut","filter","exposure_time","secz","psf","sky","cloud","t_eff"]
	filters = ['g','r','i','z','Y']
	colours = ['g','r','m','pink','y']

	for band in filters:
		y=[]
		x = exp.keys()
		xvals=[]
		times=[]
		for item in x:
			temp=float(exp[item][headers.index("psf")])
			if exp[item][headers.index("filter")]!=band:
				continue

			xvals.append(item)
			y.append(temp)
		median = np.median(y)
		fig,ax = plt.subplots()
		ax.scatter(xvals,y,marker="*",label="{} psf".format(band))
		ax.plot(xvals,[median]*len(xvals),label= "{} psf median: {}".format(band,round(median),c='k'))
		#ax.gcf().autofmt_xdate()
		plt.xlim(min(xvals),max(xvals))
		ax.set_xticklabels(xvals,rotation=90)
		#print str(median)+ "in band {}".format(band)
	plt.legend()
	plt.tight_layout()
	plt.savefig("all-band_psf.png")


def plot_filters_time(content,year,month,day,var,args):
	exp={}
	for itter in range(0,len(content)):
		line = content[itter].split()
		exp[line[0]]=line[1:]


	headers = ["ra","dec","ut","filter","exposure_time","secz","psf","sky","cloud","t_eff"]
	filters = ['g','r','i','z','Y']
	colours = ['g','r','m','pink','y']
	linestyles = ["-","--","-.",":","-"]
	fig,ax = plt.subplots()
	xmin=999999999
	xmax=0
	for band in filters:
		y=[]
		x = sorted(exp.keys())
		xvals=[]
		times=[]
		for item in x:
			try:
				temp=float(exp[item][headers.index(var)])
				if exp[item][headers.index("filter")]!=band:
					continue

				temp_time=exp[item][headers.index("ut")].split(":")
				time_object = datetime.datetime(year,month,day,int(temp_time[0]),int(temp_time[1]),0)
				times.append(time_object)
				y.append(temp)
			except (ValueError,IndexError):
				None
		median = np.median(y)
		ax.plot(times,y,marker="*",label="{} {}".format(band,var),c=colours[filters.index(band)],alpha=0.5)
		ax.plot(times,[median]*len(times),linestyle=linestyles[filters.index(band)], color=colours[filters.index(band)],label= "{} {} median: {}".format(band,var,round(median,2)))
		#ax.gcf().autofmt_xdate()
		if min(dates.date2num(times))<xmin:
			xmin=dates.date2num(min(times))
		if max(dates.date2num(times))>xmax:
			xmax=dates.date2num(max(times))
		ax.set_xticklabels(times,rotation=90)
		ax.xaxis.set_major_formatter(dates.DateFormatter('%H:%M'))
		#print str(median)+ "in band {}".format(band)
		if band=='i' and var=="psf":
			if y==[]:
				av=float("nan")
			else:
				av = np.average(y)
			print '''The average i band psf::
				Median = {} arcsec
				Mean   = {} arcsec
				RMS    = {} arcsec\n\n\n'''.format(median,av,get_rms_iband(y))
	plt.xlim(xmin,xmax)
	lgd = plt.legend(loc='center left', bbox_to_anchor=(1, 0.5),
          fancybox=True, shadow=True, ncol=1)
	#plt.tight_layout()
	plt.xlabel("Time in UT :{}-{}-{}".format(year,month,day))
	if var=="psf":
		plt.ylabel("arcsec")
	else:
		plt.ylabel(var)
	plt.savefig("all-band_{}.png".format(var),bbox_extra_artists=(lgd,), bbox_inches='tight')


def quarter_plot(content,year,month,day,var,args):
	exp={}
	for itter in range(0,len(content)):
		line = content[itter].split()
		exp[line[0]]=line[1:]


	headers = ["ra","dec","ut","filter","exposure_time","secz","psf","sky","cloud","t_eff"]
	filters = ['u','g','r','i','z','Y']
	colours = ['k','g','r','m','pink','y']
	linestyles = [":","-","--","-.",":","-"]
	all_times=[]
	for item in exp.keys():
		try:
			temp_time=exp[item][headers.index("ut")].split(":")
			time_object = datetime.datetime(year,month,day,int(temp_time[0]),int(temp_time[1]),0)
			all_times.append(dates.date2num(time_object))
		except (ValueError,IndexError):
			None
	counter=0
	q1,q2,q3,q4=get_quartiles(all_times)
	q1_time={}
	q2_time={}
	q3_time={}
	q4_time={}
	for band in filters:
		q1_time[band]=[]
		q2_time[band]=[]
		q3_time[band]=[]
		q4_time[band]=[]

	for item in exp.keys():
		try:
			psf_val=float(exp[item][headers.index(var)])
			fil = exp[item][headers.index("filter")]
			if fil not in filters:continue
			ut_h = int(exp[item][headers.index("ut")].split(":")[0])
			ut_m = int(exp[item][headers.index("ut")].split(":")[1])
			time = datetime.datetime(year,month,day,ut_h,ut_m,0)
			time_num=dates.date2num(time)
			if time_num <q1:
				q1_time[fil].append([time,psf_val])
			elif time_num >q1 and time_num<q2:
				q2_time[fil].append([time,psf_val])
			elif time_num> q2 and time_num<q3:
				q3_time[fil].append([time,psf_val])
			elif time_num > q3 and time_num<q4:
				q4_time[fil].append([time,psf_val])
		except (ValueError,IndexError):
			None

	counter=0
	for quarter in [q1_time,q2_time,q3_time,q4_time]:
		counter+=1
		fig,ax = plt.subplots()
		xmin=999999999
		xmax=0
		for band in filters:
			temp={}
			y=[]
			for itter in range(0,len(quarter[band][:])):
				temp[quarter[band][itter][0]]=quarter[band][itter][1]
			x=sorted(temp.keys())
			for item in x:
				y.append(temp[item])
			try:
				median = np.median(y)
				ax.plot(x,y,marker="*",label="{} {}".format(band,var),c=colours[filters.index(band)],alpha=0.5)
				ax.plot(x,[median]*len(x),linestyle=linestyles[filters.index(band)], color=colours[filters.index(band)],label= "{} {} median: {}".format(band,var,round(median,2)))
					#ax.gcf().autofmt_xdate()
				if min(dates.date2num(x))<xmin:
					xmin=dates.date2num(min(x))
				if max(dates.date2num(x))>xmax:
					xmax=dates.date2num(max(x))
				ax.set_xticklabels(x,rotation=90)
				ax.xaxis.set_major_formatter(dates.DateFormatter('%H:%M'))
				#print str(median)+ "in band {}".format(band)
			except (ValueError,IndexError):
				None
			if band=='i' and var=="psf":
				if y==[]:
					av=float("nan")
				else:
					av = np.average(y)
				print '''The i band psf for Q{}:
					Median = {} arcsec
					Mean   = {} arcsec
					RMS    = {} arcsec\n\n\n'''.format(counter,median,av,get_rms_iband(y))

		plt.xlim(xmin,xmax)
		lgd = plt.legend(loc='center left', bbox_to_anchor=(1, 0.5),
	          fancybox=True, shadow=True, ncol=1)
		#plt.tight_layout()
		plt.xlabel("Q{} :Time in UT :{}-{}-{}".format(counter,year,month,day))
		if var=="psf":
			plt.ylabel("arcsec")
		else:
			plt.ylabel(var)
		plt.savefig("Q{}-all_band_{}.png".format(counter,var),bbox_extra_artists=(lgd,), bbox_inches='tight')
		print

def get_statistics(content,year,month,day,args):
	exp={}
	headers = ["ra","dec","ut","filter","exposure_time","secz","psf","sky","cloud","t_eff"]
	filters = ['u','g','r','i','z','Y']
	colours = ['k','g','r','m','pink','y']

	for itter in range(0,len(content)):
		line = content[itter].split()
		if len(line)>13:
			temp_dict={}
			for var in range(0,len(headers)):
				# print(line)
				temp_dict[headers[var]]=line[var+1]
			exp[line[0]]=temp_dict
	# print(exp)
	stats = {}
	for band in filters:
		stats[band]={}
		for header in headers:
			stats[band][header]=[]
	for key in exp.keys():
		band = exp[key]["filter"]
		for head in exp[key].keys():
			if head==band or band not in filters:
				continue
			else:
				stats[band][head].append(exp[key][head])
	for band in filters:
		for head in headers:
			if band==head or stats[band][head]==[]:
				continue
			else:
				try:
					float(stats[band][head][0])
					stats[band][head]=np.array(stats[band][head],dtype=float)
				except ValueError:
					stats[band][head]=np.array(stats[band][head])
	final = {}
	for band in filters:
		final[band]={}
		teff_pro = []
		for itter in range(len(stats[band]["t_eff"])):
			teff_pro.append(stats[band]["t_eff"][itter]*stats[band]["exposure_time"][itter])
		if teff_pro==[]:
			final[band]["Sum_teff_x_Exp"]=np.nan
			final[band]["max_t_eff"]=np.nan
			final[band]["min_psf"]=np.nan
		else:
			final[band]["Sum_teff_x_Exp"]=np.sum(teff_pro)
			final[band]["max_t_eff"]=max(stats[band]["t_eff"])
			final[band]["min_psf"]=min(stats[band]["psf"])
	all_psf=[]
	all_teff=[]
	all_product=[]
	for band in filters:
		for res in stats[band]['psf']:
			all_psf.append(res)
		for res in stats[band]['t_eff']:
			all_teff.append(res)
		all_product.append(final[band]["Sum_teff_x_Exp"])

	for band in filters:
		print "Band:",band
		for key in final[band].keys():
			print "\t{k} : {r}".format(k=key,r=final[band][key])
	print("")
	print "All Night averages:"
	print "\tpsf:",np.mean(all_psf)
	print "\tt_eff:",np.mean(all_teff)
	print "\tSN Total:",np.nansum(all_product)

def get_quartiles(list):
	minu = min(list)
	diff= max(list)-min(list)
	q1=.25*diff+minu
	q2=.5*diff+minu
	q3=.75*diff+minu
	q4=diff+minu
	return q1,q2,q3,q4

def get_rms_iband(_list):
	if _list==[]:
		av=float("nan")
	else:
		av = np.average(_list)
	_sum=0
	n=float(len(_list))
	for element in _list:
		_sum+=((av - element)**2.)/n
	return str(np.sqrt(_sum))

def argparser():
	year,month,day = get_date()
	set_date = str(year)+"-"+str(month)+"-"+str(day-1)
	parser = argparse.ArgumentParser()
	parser.add_argument("--Date","-D",help="Date of the qcinv file in the format YYYY-MM-DD",default=set_date)
	parser.add_argument("--show-plots",type=bool , help="Display final summary plots, default is False", choices=[True,False],default=False)
	parser.add_argument("--WF_stats",type=str,help="Calculate psf,teff and SN for WF exposure for bragging rights", default="True")
	parser.add_argument("--All_stats",type=str,help="Calculate psf,teff and SN for all exposure for bragging rights", default="False")
	args = parser.parse_args()
	return args

def main():
	args = argparser()
	print args
	year='2018'
	month="11"
	day="26"
	print("The date used is {} in UTC. This translates to the date which qcInvPrint outputs at the end of the night.\n".format(args.Date))
	year,month,day = map(str,(args.Date).split("-"))
	try:
		with open("{}{}{}.qcinv".format(year,month,day)) as f:
			content = f.readlines()
	except IOError:
		print "No file found for today, please run qcInvPrint as observer2 in godb."
		sys.exit()
	content=content[1:-2]
	actual=[]
	for line in content:
		if "SDSS" not in line and "C26202" not in line:
			actual.append(line)
	content=actual
	quarter_plot(content,year,month,day,"psf",args)
	quarter_plot(content,year,month,day,"t_eff",args)
	plot_filters_time(content,year,month,day,"t_eff",args)
	plot_filters_time(content,year,month,day,"psf",args)

	if args.All_stats=="True":
		print "All Stats:"
		get_statistics(content,year,month,day,'')
	if args.WF_stats=="True":
		print "WF Only Statistics:"
		actual=[]
		for line in content:
			if "WF" in line and "tile" in line:
				actual.append(line)
		content=actual
		get_statistics(content,year,month,day,'')
	if args.show_plots:
		os.system('display all-band_psf.png &')
		os.system('display all-band_t_eff.png &')




if __name__ == '__main__':
	with warnings.catch_warnings():
		warnings.simplefilter("ignore", category=RuntimeWarning)
		main()
		print "Plots will be overwritten each time, if you wish to keep the plots, rename them with the date.\n\n"
