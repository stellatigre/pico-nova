from celery import task

@task()
def crawl_domain(domain_pk):
    from piconova import domain_crawl
    return domain_crawl(domain_pk)
