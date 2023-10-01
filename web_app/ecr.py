from aws_cdk import aws_ecr as ecr

def createRepositoryForImage(self):
    repository = ecr.Repository(
        self,
        "ECRRepository",
        repository_name = "imagerepo"     
    )
    
    return repository.repository_uri