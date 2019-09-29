# frozen_string_literal: true

module Blog
  # S3
  module S3
    def self.publish(path, bucket, creds)
      cmd = "aws s3 sync --delete #{path} s3://#{bucket}/"
      env = {
        'AWS_ACCESS_KEY_ID' => creds['s3_id'],
        'AWS_SECRET_ACCESS_KEY' => creds['s3_secret']
      }
      system(env, cmd)
    end
  end
end
