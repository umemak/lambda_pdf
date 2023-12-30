
# Welcome to your CDK Python project!

This is a blank project for CDK development with Python.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!


## 参考

- [LambdaでS3のPDFを画像化して保存（Docker,Python） #Python - Qiita](https://qiita.com/yosiiii/items/bb7c6793b2bdd2029b95)
- [【AWS】複数のLambdaに同条件のS3トリガーを設定したい時にハマった話 - BFT名古屋 TECH BLOG](https://bftnagoya.hateblo.jp/entry/2021/12/09/103727)
- [StepFunctions を CDK + Typescript で構築するサンプル集 - RAKSUL TechBlog](https://techblog.raksul.com/entry/2021/12/21/stepfunctions-%25e3%2582%2592-cdk-typescript-%25e3%2581%25a7%25e6%25a7%258b%25e7%25af%2589%25e3%2581%2599%25e3%2582%258b%25e3%2582%25b5%25e3%2583%25b3%25e3%2583%2597%25e3%2583%25ab%25e9%259b%2586/)
- [AWS CDK で S3 の PUT をトリガーに Step Functions 起動する構成を作成してみた | DevelopersIO](https://dev.classmethod.jp/articles/s3-put-trigger-stepfunctions/)
