#! /bin/sh                                                                                                                                            

export PATH=$PATH:/usr/local/bin

cd /home/PYPJ/IDCKX_Spider

nohup scrapy crawl idcquan >> idcquan.log 2>&1 &