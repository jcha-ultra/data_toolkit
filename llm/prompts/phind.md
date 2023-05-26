# Phind

## Image Embedding

Enables Phind to output images sometimes.

```
<Request>

Provide relevant images to help the explanation using the following formatting: ![alt text](image address)

Do not include .gif images.
```

It's not super reliable since it relies on hotlinking of images from the search results.


## Image Generation

```
You will now act as a prompt generator. 
I will describe an image to you, and you will create a prompt that could be used for image-generation. 
Once I described the image, give a 5-word summary and then include the following markdown. 

![Image](https://image.pollinations.ai/prompt/{description})

where {description} is:
{sceneDetailed}%20{adjective}%20{charactersDetailed}%20{visualStyle}%20{genre}%20{artistReference}
```
