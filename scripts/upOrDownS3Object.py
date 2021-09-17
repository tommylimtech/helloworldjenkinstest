#!/bin/python3

### This script is used to upload or download an object from S3 ###

# Import Necessary Modules
from datetime import datetime
import logging,argparse,sys,os
import boto3  # This is installed using pip

# Set Arguments
parser = argparse.ArgumentParser()
parser.add_argument("-r", "--region", help = "AWS Region. Default is defined in credentials file")
parser.add_argument("-b", "--bucket", help = "S3 Bucket Name", required=True)
parser.add_argument("-o", "--object", help = "S3 Object. Full Path to Object/File", required=True)
parser.add_argument("-u", "--upload", help = "Boolean - If set, upload object to S3. Default without flag is to download object", action='store_true')
#parser.add_argument("-d", "--download", help = "Download object from S3")
parser.add_argument("-l", "--loglevel", help = "Set Logging Level. Defaults to WARNING", choices=['DEBUG','INFO','WARNING','ERROR','CRITICAL'])
# Parse Arguments
args = parser.parse_args()

# Set Log Level
if args.loglevel != None:
    logging.basicConfig(level=args.loglevel)

# Create Logger
logger = logging.getLogger("test-python.py")

# Functions
def uploadToS3 (region, bucket, object_file, logger):
    # Function to upload a file to S3
    try:
        # Convert filename from local system to an object type for s3
        object = os.path.basename(object_file)
        # Initialize s3 client
        s3 = boto3.client('s3')
        # Attempt to upload file
        response = s3.upload_file(object_file, bucket, object)
        # Log response
        logger.info("[%s]: Uploaded object. Response: %s" % (datetime.now(),response))
    except Exception as e:
        logger.exception("[%s]: %s" % (datetime.now(),str(e)))
    except:
        logger.exception(sys.exc_info())

def downloadFromS3 (region, bucket, object, logger):
    # Function to download an object from S3
    try:
        # Initialize s3 client
        s3 = boto3.client('s3')
        # Attempt to download object
        response = s3.download_file(bucket, object, object)
        # Log response
        logger.info("[%s]: Downloaded object. Response: %s" % (datetime.now(),response))
    except Exception as e:
        logger.exception("[%s]: %s" % (datetime.now(),str(e)))
    except:
        logger.exception(sys.exc_info())

# Print Debugging info
print("hello world")
logger.debug("[%s]: Args" % datetime.now())
logger.debug("[%s]: \tRegion: %s" % (datetime.now(),args.region))
logger.debug("[%s]: \tBucket: %s" % (datetime.now(),args.bucket))
logger.debug("[%s]: \tObject: %s" % (datetime.now(),args.object))
logger.debug("[%s]: \tUpload: %s" % (datetime.now(),args.upload))
#logger.debug("[%s]: \tDownload: %s" % (datetime.now(),args.download))
logger.debug("[%s]: \tLog Level: %s" % (datetime.now(),args.loglevel))

# What to do depends on "-u" argument
if args.upload is True:
    uploadToS3(args.region, args.bucket, args.object, logger)
else:
    downloadFromS3(args.region, args.bucket, args.object, logger)

print("script complete")
