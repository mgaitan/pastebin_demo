

    parser = init_argparse()
    args = parser.parse_args(args)

    try:
        repo, user = get_repo_and_user()
    except Exception as e:
        print(f"Ensure SHBIN_GITHUB_TOKEN and SHBIN_REPO environment variables are correctly set. (error {e})")
        sys.exit(-1)

    files = args.files
    