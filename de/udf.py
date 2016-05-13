import sys
from get_logger import get_logger
import traceback

logger = get_logger('udf')

for line in sys.stdin:
	segs = line.strip().split('\t')
	if len(segs) == 5:
		try:
			uid, paytimes, payamount, payrecord, date_diff, loginrecord, duration, logintimes = line.strip().split('\t')
			payamount_d30 = []
			paytimes_d30 = []
			for i in payrecord.split(','):
				payamount_d30.append(float(i.split(':')[2]))
				paytimes_d30.append(int(i.split(':')[1]))
			logintimes_d30 = []
			duration_d30 = []
			for j in loginrecord.split(','):
				logintimes_d30.append(int(j.split(':')[1]))
				duration_d30.append(int(j.split(':')[2]))
			print "\t".join([uid, paytimes, payamount, str(sum(paytimes_d30)), str(sum(payamount_d30)), str(sum(logintimes_d30)), str(sum(duration_d30)) date_diff])
		except Exception, e:
			logger.error(traceback.format_exc())
