#!/bin/sh
TARGET=""
rsync -r -a -d --progress --  public/* ${TARGET}
