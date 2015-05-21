import sys
import random
import math
import re, math, collections
import os
import csv
import fnmatch

def logLikelihood(docTermDic, topicDic, topicTermDic, docTopicDic):
	result = 0
	for docID in docTermDic:
		for termID, value in docTermDic[docID].iteritems():
			pdw = 0
			for topicID in topicDic:
				pdw += (topicTermDic[topicID][termID] * docTopicDic[docID][topicID] / topicDic[topicID])
			result += value * math.log(pdw)
	return result

def pLSA(docTermDic, termDocDic, nTopics, maxIterations, threshold, outfile):
        print 'initialization...'
        file_write = open(outfile, 'a')
        beta = 0
        betaInc = (1.0-beta)/maxIterations

        nDocs = len(docTermDic)
        nTerms = len(termDocDic)

        # initialized N(w,z) and N(z)
        topicTermDic = {}
        topicDic = {}
        for topicID in xrange(nTopics):
                topicTermDic[topicID] = {}
                normalization = 0
                for termID in termDocDic:
                        nominator = random.random()
                        topicTermDic[topicID][termID] = nominator
                        normalization += nominator
                topicDic[topicID] = normalization

        # initialize p(z|d)
        docTopicDic = {}
        docTopicNormalizationDic = {}
        for docID in docTermDic:
                docTopicDic[docID] = {}
                normalization = 0
                for topicID in xrange(nTopics):
                        nominator = random.random()
                        docTopicDic[docID][topicID] = nominator
                        normalization += nominator
                docTopicNormalizationDic[docID] = normalization

        # initialized new N(w,z) and N(z)
        topicTermDic2 = {}
        topicDic2 = {}
        for topicID in xrange(nTopics):
                topicTermDic2[topicID] = {}
                for termID in termDocDic:
                        topicTermDic2[topicID][termID] = 0
                topicDic2[topicID] = 0

        # initialize new p(z|d)
        docTopicDic2 = {}
        docTopicNormalizationDic2 = {}
        for docID in docTermDic:
                docTopicDic2[docID] = {}
                for topicID in xrange(nTopics):
                        docTopicDic2[docID][topicID] = 0
                docTopicNormalizationDic2[docID] = 0

        preLogLikelihood = None
        metThreshold = 0
        endIteration = 0
        for itr in xrange(maxIterations):
                print itr

                beta += betaInc

                # initialized new N(w,z) and N(z)
                for topicID in xrange(nTopics):
                        for termID in termDocDic:
                                topicTermDic2[topicID][termID] = 0
                        topicDic2[topicID] = 0

                # initialize new p(z|d)
                for docID in docTermDic:
                        normalization = 0
                        for topicID in xrange(nTopics):
                                docTopicDic2[docID][topicID] = 0
                        docTopicNormalizationDic2[docID] = 0

                # p(z|d,w)
                for docID in docTermDic:
                        for termID, value in docTermDic[docID].iteritems():
                                normalization = 0
                                tmpDocTermTopicDic = {}
                                for topicID in xrange(nTopics):
                                        nominator = math.exp(math.log(docTopicDic[docID][topicID] * topicTermDic[topicID][termID] / (topicDic[topicID] * docTopicNormalizationDic[docID])) * beta)
                                        tmpDocTermTopicDic[topicID] = nominator
                                        normalization += nominator
                                if normalization <> 0:
                                        for topicID in xrange(nTopics):
                                                tmpDocTermTopicDic[topicID] /= normalization

                                                # update N(w, z)
                                                topicTermDic2[topicID][termID] += tmpDocTermTopicDic[topicID]
                                                # update N(z)
                                                topicDic2[topicID] += tmpDocTermTopicDic[topicID]
                                                # update p(z|d)
                                                docTopicDic2[docID][topicID] += tmpDocTermTopicDic[topicID]
                                                docTopicNormalizationDic2[docID] += tmpDocTermTopicDic[topicID]

                # N(w, z) N(z)
                tmpDic = topicTermDic
                topicTermDic = topicTermDic2
                topicTermDic2 = tmpDic

                tmpDic = topicDic
                topicDic = topicDic2
                topicDic2 = tmpDic

                # p(z|d)
                tmpDic = docTopicDic
                docTopicDic = docTopicDic2
                docTopicDic2 = tmpDic

                tmpDic = docTopicNormalizationDic
                docTopicNormalizationDic = docTopicNormalizationDic2
                docTopicNormalizationDic2 = tmpDic

        #		curLogLikelihood = logLikelihood(docTermDic, topicDic, topicTermDic, docTopicDic)
        #		if preLogLikelihood is not None:
        #			if math.fabs(preLogLikelihood - curLogLikelihood) < threshold:
        #				metThreshold = 1
        #				break
        #		preLogLikelihood = curLogLikelihood
        #		endIteration = itr
        #		print curLogLikelihood

        # output p(z|d,w)
        print 'docID, termID, topicID: p(z|d,w)'
        for docID in docTermDic:
                for termID, value in docTermDic[docID].iteritems():
                        normalization = 0
                        tmpDocTermTopicDic = {}
                        for topicID in xrange(nTopics):
                                nominator = docTopicDic[docID][topicID] * topicTermDic[topicID][termID] / topicDic[topicID]
                                tmpDocTermTopicDic[topicID] = nominator
                                normalization += nominator
                        if normalization <> 0:
                                for topicID in xrange(nTopics):
                                        tmpDocTermTopicDic[topicID] /= normalization
                        for topicID, prob in tmpDocTermTopicDic.iteritems():
                                #print '%s %s %s: %f' % (docID, termID, topicID, prob)
                                file_write.write(str(docID) + " " + str(termID) + " " + str(topicID) + " " + str(prob)+ "\n")

        # output p(z|d)
        print 'docID, topicID: p(z|d)'
        for docID in docTopicDic:
                for topicID, prob in docTopicDic[docID].iteritems():
                        #print '%s %s: %f' % (docID, topicID, prob)
                        file_write.write(str(docID) + " " + str(topicID)+ " " + str(prob)+ "\n")
        # output N(z, w)
        print 'topicID, termID: N(z, w)'
        for topicID in topicTermDic:
                for termID, prob in topicTermDic[topicID].iteritems():
                        #print '%s %s: %s' % (topicID, termID, prob)
                        file_write.write(str(topicID) + " " + str(termID)+ " " + str(prob)+ "\n")
        # output p(z)
        print 'topicID: N(z), p(z)'
        normalization = 0
        for topicID in topicDic:
                normalization += topicDic[topicID]             
        for topicID, prob in topicDic.iteritems():
                #print type(normalization)
                print '%s: %f %f' % (topicID, prob, prob/normalization)
                file_write.write(str(topicID) + " " + str(prob)+ " " + str(prob/normalization)+ "\n")
	# output log-likelihood
#	print 'log-likelihood: %s, threshold met: %d, end iteration: %d' % (curLogLikelihood, metThreshold, endIteration)

##if __name__ == '__main__':
##	if len(sys.argv) < 5:
##		print 'usage: python pLSA.py dataFile nTopics maxIterations threshold'
##		exit(1)

def run_PLSA(filename, files):
        docTermDic = {}
        termDocDic = {}
        lineNo = 0
        for line in open(filename):
                lineNo += 1
                parts = line.strip().split();
                docID = parts[0]
                #print parts
                termIDs = parts[1:]
                value = 1.0
                for item in termIDs:
                        termID = item
                        if docTermDic.has_key(docID):
                                docTermDic[docID][termID] = value
                        else:
                                docTermDic[docID] = dict([(termID, value)])
                        if termDocDic.has_key(termID):
                                termDocDic[termID][docID] = value
                        else:
                                termDocDic[termID] = dict([(docID, value)])
        print 'read %d lines, %d documents, and %d words.' % (lineNo, len(docTermDic), len(termDocDic))
        #nTopics = int(sys.argv[2])
        nTopics =10
        #maxIterations = int(sys.argv[3])
        maxIterations=10
        #threshold = float(sys.argv[4])
        threshold = 0.05
        outfile = "/home/sbasu/Videopedia_MM/PLSA_recal/VideoPLSI/" + files
        pLSA(docTermDic, termDocDic, nTopics, maxIterations, threshold, outfile)


path_wiki = '/home/sbasu/Videopedia_MM/extractedWords/'

for files in os.listdir(path_wiki):
    file_to_open = path_wiki + files
    print files
##    f = open(file_to_open, 'r')
##    d = f.read()
    run_PLSA(file_to_open,files)
