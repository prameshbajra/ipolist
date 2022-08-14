# ipolist

Activate the virtual env:
```
conda activate <nameofvenv>
```

For deploying:

```
sam build && sam deploy
```

For testing locally:

```
# Export path for test to find the source code ....
export PYTHONPATH='/Users/prameshbajracharya/lecodage/personalworks/ipolisting'

# Export env vars that lambda will use
export emails_to_send='yccgpzaixr@scpulse.com,gthbpahyukbtns@knowledgemd.com,vyorwfydebrn@knowledgemd.com'

# Call function
python tests/listing.py
```