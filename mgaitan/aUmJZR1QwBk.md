
    
    if not args.files:
        """read from clipboard"""
        content = pyclip.paste()
        mime_type = magic.from_buffer(content, mime=True)
        suffix = "md" if mime_type == 'text/plain' else mime_type.split("/")[1]
        
        path_name = f"{secrets.token_urlsafe(8)}.{suffix}"
        result = repo.create_file(f"{user}/{path_name}", args.message, content)
        print(result["content"].html_url)
        return