import requests
import os
from urllib.parse import unquote
from pathlib import Path

def descargar_imagenes():
    # Lista de URLs proporcionada
    urls = [
        "https://assets.bytebytego.com/diagrams/0147-cloud-evolution.png",
        "https://assets.bytebytego.com/diagrams/0310-qr-code.jpg",
        "https://assets.bytebytego.com/diagrams/0253-learn-linux.png",
        "https://assets.bytebytego.com/diagrams/0008-6-software-architectural-patterns-you-must-know.png",
        "https://assets.bytebytego.com/diagrams/0161-database-scaling-cheatsheet.png",
        "https://assets.bytebytego.com/diagrams/0010-common-system-design-problems-and-solutions.png",
        "https://assets.bytebytego.com/diagrams/0181-eight-ds-db.jpg",
        "https://assets.bytebytego.com/diagrams/0011-8-key-concepts-in-ddd.png",
        "https://assets.bytebytego.com/diagrams/0294-oo-concepts.png",
        "https://assets.bytebytego.com/diagrams/0013-8-must-know-strategies-to-scale-your-system.png",
        "https://assets.bytebytego.com/diagrams/0019-9-best-practices-for-building-microservices.png",
        "https://assets.bytebytego.com/diagrams/0275-micro-best-practices.png",
        "https://assets.bytebytego.com/diagrams/0016-9-docker-best-practices-you-must-know.png",
        "https://assets.bytebytego.com/diagrams/0020-9-essential-components-of-production-microservice-app.png",
        "https://assets.bytebytego.com/diagrams/0023-10-books-every-software-engineer-should-read.png",
        "https://assets.bytebytego.com/diagrams/0051-10-good-coding-principles.png",
        "https://assets.bytebytego.com/diagrams/0024-10-data-structures-used-in-daily-life.png",
        "https://assets.bytebytego.com/diagrams/0026-10-system-design-trade-offs-you-cannot-ignore.png",
        "https://assets.bytebytego.com/diagrams/0243-junior-to-senior-developer-roadmap.png",
        "https://assets.bytebytego.com/diagrams/0029-15-open-source-projects-that-changed-the-world.png",
        "https://assets.bytebytego.com/diagrams/0032-oo-patterns-you-should-know.png",
        "https://assets.bytebytego.com/diagrams/0034-20-popular-open-source-projects-by-big-tech.png",
        "https://assets.bytebytego.com/diagrams/0419-25-papers-that-completely-transformed-the-computer-world.png",
        "https://assets.bytebytego.com/diagrams/0039-30-useful-ai-apps-that-can-help-you-in-2025.png",
        "https://assets.bytebytego.com/diagrams/0025-a-beginner-s-guide-to-cdn.png",
        "https://assets.bytebytego.com/diagrams/0305-programming-languages.png",
        "https://assets.bytebytego.com/diagrams/0305-programming-languages.png",
        "https://assets.bytebytego.com/diagrams/0139-cheat-sheet-for-fault-tolerant-systems.png",
        "https://assets.bytebytego.com/diagrams/0352-a-cheat-sheet-for-system-designs.png",
        "https://assets.bytebytego.com/diagrams/0399-a-cheatsheet-for-uml-class-diagrams.png",
        "https://assets.bytebytego.com/diagrams/0062-a-cheatsheet-on-database-performance.png",
        "https://assets.bytebytego.com/diagrams/0063-a-cheatsheet-on-infrastructure-as-code-landscape.png",
        "https://assets.bytebytego.com/diagrams/0065-a-crash-course-on-database-sharding.png",
        "https://assets.bytebytego.com/diagrams/0293-a-crash-course-on-architectural-scalability.png",
        "https://assets.bytebytego.com/diagrams/0199-full-stack-developer-roadmap.png",
        "https://assets.bytebytego.com/diagrams/0068-algorithms-geo-hash-linkedin.jpg",
        "https://assets.bytebytego.com/diagrams/0328-serverless-to-monolithic.jpeg",
        "https://assets.bytebytego.com/diagrams/0082-aws-cloud-services-cheat-sheet.png",
        "https://assets.bytebytego.com/diagrams/0081-aws-services-evolution.png",
        "https://assets.bytebytego.com/diagrams/0083-azure-cloud-services-cheat-sheet.png",
        "https://assets.bytebytego.com/diagrams/0091-btree-lsm.png",
        "https://assets.bytebytego.com/diagrams/0086-big-data-pipeline-cheatsheet-for-aws-azure-and-gcp.png",
        "https://assets.bytebytego.com/diagrams/0084-big-endian-vs-little-endian.png",
        "https://assets.bytebytego.com/diagrams/0088-blocking-noblocking-queue.jpeg",
        "https://assets.bytebytego.com/diagrams/0314-redis-chat.jpg",
        "https://assets.bytebytego.com/diagrams/0128-cache-miss-attack.png",
        "https://assets.bytebytego.com/diagrams/0418-cache-systems-every-developer-should-know.jpeg",
        "https://assets.bytebytego.com/diagrams/0130-can-kafka-lose-messages.png",
        "https://assets.bytebytego.com/diagrams/0350-cap-base-solid-kiss.png",
        "https://assets.bytebytego.com/diagrams/0131-cap-theorem.jpeg",
        "https://assets.bytebytego.com/diagrams/0133-change-data-capture-key-to-leverage-real-time-data.png",
        "https://assets.bytebytego.com/diagrams/0273-metrics-access-pattern.jpg",
        "https://assets.bytebytego.com/diagrams/0140-ci-cd-pipeline.png",
        "https://assets.bytebytego.com/diagrams/0141-ci-cd-workflow.png",
        "https://assets.bytebytego.com/diagrams/0093-cloud-comparison-cheat-sheet.png",
        "https://assets.bytebytego.com/diagrams/0145-cloud-cost-reduction-techniques.png",
        "https://assets.bytebytego.com/diagrams/0146-cloud-dbs2.png",
        "https://assets.bytebytego.com/diagrams/0050-cloud-disaster-recovery-strategies.png",
        "https://assets.bytebytego.com/diagrams/0094-cloud-load-balancer-cheatsheet.gif",
        "https://assets.bytebytego.com/diagrams/0095-cloud-monitoring-cheat-sheet.png",
        "https://assets.bytebytego.com/diagrams/0070-cloud-native-anti-patterns.png",
        "https://assets.bytebytego.com/diagrams/0150-concurrency-is-not-parallelism.png",
        "https://assets.bytebytego.com/diagrams/0151-consistent-hashing.png",
        "https://assets.bytebytego.com/diagrams/0155-cookies-vs-sessions-vs-jwt-vs-paseto.png",
        "https://assets.bytebytego.com/diagrams/0156-cybersecurity-101-in-one-picture.png",
        "https://assets.bytebytego.com/diagrams/0276-middleware-png.png",
        "https://assets.bytebytego.com/diagrams/0165-delivery-semantics.png",
        "https://assets.bytebytego.com/diagrams/0184-email.jpg",
        "https://assets.bytebytego.com/diagrams/0207-google-maps.png",
        "https://assets.bytebytego.com/diagrams/0167-design-patterns-cheat-sheet-part-2.png",
        "https://assets.bytebytego.com/diagrams/0344-stock-exchange.png",
        "https://assets.bytebytego.com/diagrams/0099-devops-vs-noops.png",
        "https://assets.bytebytego.com/diagrams/0172-devops-sre-platform.png",
        "https://assets.bytebytego.com/diagrams/0173-diagrams-as-code-twitter.jpeg",
        "https://assets.bytebytego.com/diagrams/0188-event-sourcing.jpeg",
        "https://assets.bytebytego.com/diagrams/0087-blockchains.png",
        "https://assets.bytebytego.com/diagrams/0175-dns-record-types-you-should-know.png",
        "https://assets.bytebytego.com/diagrams/0363-do-you-know-why-meta-google-and-amazon-all-stop-using-leap-seconds.jpeg",
        "https://assets.bytebytego.com/diagrams/0179-e-commerce-works.png",
        "https://assets.bytebytego.com/diagrams/0033-encoding-vs-encryption-vs-tokenization.png",
        "https://assets.bytebytego.com/diagrams/0187-erasure-coding.png",
        "https://assets.bytebytego.com/diagrams/0117-explain-the-top-6-use-cases-of-object-stores.png",
        "https://assets.bytebytego.com/diagrams/0006-explaining-5-unique-id-generators-in-distributed-systems.png",
        "https://assets.bytebytego.com/diagrams/0292-explaining-8-popular-network-protocols-in-1-diagram.png",
        "https://assets.bytebytego.com/diagrams/0107-explaining-json-web-token-jwt-to-a-10-year-old-kid.png",
        "https://assets.bytebytego.com/diagrams/0330-session-square.png",
        "https://assets.bytebytego.com/diagrams/0366-types-of-queues.png",
        "https://assets.bytebytego.com/diagrams/0191-firewall.jpeg",
        "https://assets.bytebytego.com/diagrams/0194-foreign-exchange.png",
        "https://assets.bytebytego.com/diagrams/0201-git-commands-cheat-sheet.png",
        "https://assets.bytebytego.com/diagrams/0203-git-merge-git-rebase.jpg",
        "https://assets.bytebytego.com/diagrams/0204-git-vs-github.png",
        "https://assets.bytebytego.com/diagrams/0205-git-workflow.jpg",
        "https://assets.bytebytego.com/diagrams/0212-hotspot-accounts.png",
        "https://assets.bytebytego.com/diagrams/0148-cloud-hidden-costs.png",
        "https://assets.bytebytego.com/diagrams/0002-apple-pay.jpg",
        "https://assets.bytebytego.com/diagrams/0309-push-notifiction.jpg",
        "https://assets.bytebytego.com/diagrams/0038-how-caches-can-go-wrong.png",
        "https://assets.bytebytego.com/diagrams/0388-how-can-redis-be-used.png",
        "https://assets.bytebytego.com/diagrams/0219-how-digital-signatures-work.png",
        "https://assets.bytebytego.com/diagrams/0216-how-airtag-works.png",
        "https://assets.bytebytego.com/diagrams/0085-big-keys.png",
        "https://assets.bytebytego.com/diagrams/0003-how-python-works.png",
        "https://assets.bytebytego.com/diagrams/0334-ship-to-prod.png",
        "https://assets.bytebytego.com/diagrams/0218-how-do-computer-programs-run.png",
        "https://assets.bytebytego.com/diagrams/0347-street-view-blurring-system.png",
        "https://assets.bytebytego.com/diagrams/0271-message-queue-evolve.png",
        "https://assets.bytebytego.com/diagrams/0234-inter-process-communication.png",
        "https://assets.bytebytego.com/diagrams/0103-how-do-search-engines-work.png",
        "https://assets.bytebytego.com/diagrams/0367-top-4-types-of-sql-joins.png",
        "https://assets.bytebytego.com/diagrams/0134-chat-app.jpeg",
        "https://assets.bytebytego.com/diagrams/0300-permission-systems.png",
        "https://assets.bytebytego.com/diagrams/0138-cheat-sheet-for-designing-secure-systems.png",
        "https://assets.bytebytego.com/diagrams/0235-internationalization.jpeg",
        "https://assets.bytebytego.com/diagrams/0211-high-availability.jpg",
        "https://assets.bytebytego.com/diagrams/0370-top-6-heartbeat-detection-mechanisms.png",
        "https://assets.bytebytego.com/diagrams/0037-use-cases-for-event-sourcing.png",
        "https://assets.bytebytego.com/diagrams/0182-elastic-search.jpeg",
        "https://assets.bytebytego.com/diagrams/0056-how-we-manage-configuration.png",
        "https://assets.bytebytego.com/diagrams/0379-top-6-data-management-patterns.png",
        "https://assets.bytebytego.com/diagrams/0058-cheatsheet-for-managing-sensitive-data.png",
        "https://assets.bytebytego.com/diagrams/0229-how-do-we-retry-on-failures.png",
        "https://assets.bytebytego.com/diagrams/0149-how-doe-we-adopt-cloud-native.png",
        "https://assets.bytebytego.com/diagrams/0160-database-types.jpg",
        "https://assets.bytebytego.com/diagrams/0297-password-manager.png",
        "https://assets.bytebytego.com/diagrams/0052-how-a-vpn-works.png",
        "https://assets.bytebytego.com/diagrams/0067-how-does-ach-payment-work.png",
        "https://assets.bytebytego.com/diagrams/0069-amazon-build-system.jpeg",
        "https://assets.bytebytego.com/diagrams/0249-lambda.jpg",
        "https://assets.bytebytego.com/diagrams/0230-how-cdn-works.png",
        "https://assets.bytebytego.com/diagrams/0414-how-does-docker-work.png",
        "https://assets.bytebytego.com/diagrams/0200-garbage-collection-101.png",
        "https://assets.bytebytego.com/diagrams/0202-git-commands.png",
        "https://assets.bytebytego.com/diagrams/0079-authenticator.jpg",
        "https://assets.bytebytego.com/diagrams/0220-how-does-https-work.png",
        "https://assets.bytebytego.com/diagrams/0214-how-redis-presists-data.png",
        "https://assets.bytebytego.com/diagrams/0323-scan-to-pay.png",
        "https://assets.bytebytego.com/diagrams/0224-how-does-ssh-work.png",
        "https://assets.bytebytego.com/diagrams/0225-how-terraform-creates-infra-at-scale.png",
        "https://assets.bytebytego.com/diagrams/0176-dns-look-up.png",
        "https://assets.bytebytego.com/diagrams/0041-how-does-visa-make-money.png",
        "https://assets.bytebytego.com/diagrams/0403-visa-payment.jpg",
        "https://assets.bytebytego.com/diagrams/0340-sql-execution-order-in-db.jpeg",
        "https://assets.bytebytego.com/diagrams/0159-data-transfer-between-apps.png",
        "https://assets.bytebytego.com/diagrams/0185-email-deliver.png",
        "https://assets.bytebytego.com/diagrams/0223-how-redis-architecture-evolve.png",
        "https://assets.bytebytego.com/diagrams/0104-how-to-ace-system-design-interviews-like-a-boss.png",
        "https://assets.bytebytego.com/diagrams/0089-bloomfilter.png",
        "https://assets.bytebytego.com/diagrams/0178-double-charge.jpg",
        "https://assets.bytebytego.com/diagrams/0227-how-to-choose-the-right-database.png",
        "https://assets.bytebytego.com/diagrams/0166-deployment-strategies.png",
        "https://assets.bytebytego.com/diagrams/0206-google-doc.png",
        "https://assets.bytebytego.com/diagrams/0144-client-handle-error.png",
        "https://assets.bytebytego.com/diagrams/0162-database-middleware.png",
        "https://assets.bytebytego.com/diagrams/0254-learn-payment.png",
        "https://assets.bytebytego.com/diagrams/0198-frontend-performance-cheatsheet.png",
        "https://assets.bytebytego.com/diagrams/0228-how-to-release-a-mobile-app.png",
        "https://assets.bytebytego.com/diagrams/0322-scale-to-million.jpg",
        "https://assets.bytebytego.com/diagrams/0321-salt.png",
        "https://assets.bytebytego.com/diagrams/0284-multipart-upload.png",
        "https://assets.bytebytego.com/diagrams/0153-cookies.png",
        "https://assets.bytebytego.com/diagrams/0409-https-ssl-handshake-and-data-encryption-explained-to-kids.png",
        "https://assets.bytebytego.com/diagrams/0035-imperative-vs-functional-vs-oop.png",
        "https://assets.bytebytego.com/diagrams/0236-ipv4-vs-ipv6.png",
        "https://assets.bytebytego.com/diagrams/0215-how-to-choose-db.png",
        "https://assets.bytebytego.com/diagrams/0238-is-https-reliable.png",
        "https://assets.bytebytego.com/diagrams/0406-how-wasm-work.jpeg",
        "https://assets.bytebytego.com/diagrams/0278-monolithic-arch-use-cases.jpg",
        "https://assets.bytebytego.com/diagrams/0296-is-passkey-shaping-a-passwordless-future.png",
        "https://assets.bytebytego.com/diagrams/0237-is-postgresql-eating-the-database-world.png",
        "https://assets.bytebytego.com/diagrams/0240-java-collection.png",
        "https://assets.bytebytego.com/diagrams/0242-json-crack.png",
        "https://assets.bytebytego.com/diagrams/0244-jwt-101-key-to-stateless-authentication.png",
        "https://assets.bytebytego.com/diagrams/0096-dbshards.png",
        "https://assets.bytebytego.com/diagrams/0163-ddd.png",
        "https://assets.bytebytego.com/diagrams/0247-kubernates-deployment-strategy.jpeg",
        "https://assets.bytebytego.com/diagrams/0108-kubernetes-periodic-table.png",
        "https://assets.bytebytego.com/diagrams/0109-kubernetes-tools-ecosystem.png",
        "https://assets.bytebytego.com/diagrams/0110-kubernetes-tools-stack-wheel.png",
        "https://assets.bytebytego.com/diagrams/0004-learn-cache.png",
        "https://assets.bytebytego.com/diagrams/0256-life-is-short-use-dev-tools.png",
        "https://assets.bytebytego.com/diagrams/0213-linux-boot-process-explained.png",
        "https://assets.bytebytego.com/diagrams/0259-linux-permissions-copy.png",
        "https://assets.bytebytego.com/diagrams/0258-linux-file-system-explained.jpg",
        "https://assets.bytebytego.com/diagrams/0260-live-streaming-updated.png",
        "https://assets.bytebytego.com/diagrams/0263-log-parsing.png",
        "https://assets.bytebytego.com/diagrams/0264-logging-tracing-metrics.png",
        "https://assets.bytebytego.com/diagrams/0265-low-latency-stock-exchange.jpg",
        "https://assets.bytebytego.com/diagrams/0326-seo.jpg",
        "https://assets.bytebytego.com/diagrams/0267-memcached-redis.jpg",
        "https://assets.bytebytego.com/diagrams/0127-buy-something-money-movement.jpg",
        "https://assets.bytebytego.com/diagrams/0279-monorepo-microrepo.png",
        "https://assets.bytebytego.com/diagrams/0281-most-popular-cache-eviction.png",
        "https://assets.bytebytego.com/diagrams/0283-most-used-linux.png",
        "https://assets.bytebytego.com/diagrams/0285-must-know-system-design-building-blocks.png",
        "https://assets.bytebytego.com/diagrams/0143-client-arch-patterns.png",
        "https://assets.bytebytego.com/diagrams/0353-my-recommended-materials-for-cracking-your-next-technical-interview.png",
        "https://assets.bytebytego.com/diagrams/0111-what-is-oauth.png",
        "https://assets.bytebytego.com/diagrams/0112-oauth-flows.png",
        "https://assets.bytebytego.com/diagrams/0113-orchestration-vs-choreography-microservices.png",
        "https://assets.bytebytego.com/diagrams/0170-dev-tester-ratio.png",
        "https://assets.bytebytego.com/diagrams/0299-payment-system.jpeg",
        "https://assets.bytebytego.com/diagrams/0301-pessimistic-vs-optimistic-locking.png",
        "https://assets.bytebytego.com/diagrams/0189-experiment-framework.jpg",
        "https://assets.bytebytego.com/diagrams/0306-proximity-service-design.jpg",
        "https://assets.bytebytego.com/diagrams/0274-metrics-push-pull.png",
        "https://assets.bytebytego.com/diagrams/0311-quadtree.jpg",
        "https://assets.bytebytego.com/diagrams/0312-read-replica-pattern.png",
        "https://assets.bytebytego.com/diagrams/0298-payment-reconciliation.jpg",
        "https://assets.bytebytego.com/diagrams/0316-reliciency-patterns.jpg",
        "https://assets.bytebytego.com/diagrams/0152-cookies-session-jwt.png",
        "https://assets.bytebytego.com/diagrams/0080-avro.png",
        "https://assets.bytebytego.com/diagrams/0171-dev-ops-books.jpg",
        "https://assets.bytebytego.com/diagrams/0346-storage-system.png",
        "https://assets.bytebytego.com/diagrams/0348-swift-payment-messaging-system.png",
        "https://assets.bytebytego.com/diagrams/0349-symmetric-encryption-vs-asymmetric-encryption.png",
        "https://assets.bytebytego.com/diagrams/0324-system-design-blueprint.png",
        "https://assets.bytebytego.com/diagrams/0351-system-design-cheat-sheet.png",
        "https://assets.bytebytego.com/diagrams/0018-9-algorithms-that-dominate-our-world.png",
        "https://assets.bytebytego.com/diagrams/0028-12-factor-app.png",
        "https://assets.bytebytego.com/diagrams/0197-4-fundamental-pillars-of-object-oriented-programming.png",
        "https://assets.bytebytego.com/diagrams/0360-the-payments-ecosystem.png",
        "https://assets.bytebytego.com/diagrams/0246-kafka-101-8-steps-to-learn-the-fundamentals-of-kafka.png",
        "https://assets.bytebytego.com/diagrams/0248-kubernetes-command-cheatsheet.png",
        "https://assets.bytebytego.com/diagrams/0009-steps-to-learn-the-fundamentals-of-redis-101.png",
        "https://assets.bytebytego.com/diagrams/0118-the-ultimate-software-architect-knowledge-map.png",
        "https://assets.bytebytego.com/diagrams/0362-things-to-consider-when-using-cache.png",
        "https://assets.bytebytego.com/diagrams/0364-time-series-db-tsdb-in-20-lines.jpeg",
        "https://assets.bytebytego.com/diagrams/0331-session-cookie-jwt.jpg",
        "https://assets.bytebytego.com/diagrams/0373-top-4-data-sharding-algorithms-explained.png",
        "https://assets.bytebytego.com/diagrams/0078-authentication-mechanisms.png",
        "https://assets.bytebytego.com/diagrams/0005-4-k8s-service-types.png",
        "https://assets.bytebytego.com/diagrams/0044-top-4-udp-use-cases.png",
        "https://assets.bytebytego.com/diagrams/0374-top-5-caching-strategies.png",
        "https://assets.bytebytego.com/diagrams/0001-how-to-improve-api-performance.png",
        "https://assets.bytebytego.com/diagrams/0368-top-5-kafka-use-cases.png",
        "https://assets.bytebytego.com/diagrams/0358-the-most-popular-deployment-strategies.png",
        "https://assets.bytebytego.com/diagrams/0339-software-architecture-styles.png",
        "https://assets.bytebytego.com/diagrams/0375-top-5-strategies-to-reduce-latency.png",
        "https://assets.bytebytego.com/diagrams/0376-top-5-trade-offs-in-system-designs.png",
        "https://assets.bytebytego.com/diagrams/0377-top-6-cases-of-leveraging-idempotency.png",
        "https://assets.bytebytego.com/diagrams/0378-top-6-cloud-messaging-patterns.png",
        "https://assets.bytebytego.com/diagrams/0369-top-6-database-models.png",
        "https://assets.bytebytego.com/diagrams/0380-top-6-elasticsearch-use-cases.png",
        "https://assets.bytebytego.com/diagrams/0047-top-6-firewall-use-cases.png",
        "https://assets.bytebytego.com/diagrams/0251-lb-algorithms.png",
        "https://assets.bytebytego.com/diagrams/0327-server-types.png",
        "https://assets.bytebytego.com/diagrams/0381-top-6-multithreading-design-patterns-you-must-know.png",
        "https://assets.bytebytego.com/diagrams/0382-top-6-tools-to-turn-code-into-beautiful-diagrams.png",
        "https://assets.bytebytego.com/diagrams/0119-top-7-most-used-distributed-system-patterns.png",
        "https://assets.bytebytego.com/diagrams/0384-top-8-c-use-cases.png",
        "https://assets.bytebytego.com/diagrams/0059-top-8-cache-eviction-strategies.png",
        "https://assets.bytebytego.com/diagrams/0012-8-must-know-docker-concepts.png",
        "https://assets.bytebytego.com/diagrams/0120-top-8-programming-paradigms-2.png",
        "https://assets.bytebytego.com/diagrams/0015-8-standards-developers-should-know.png",
        "https://assets.bytebytego.com/diagrams/0387-top-9-system-integrations.png",
        "https://assets.bytebytego.com/diagrams/0386-top-9-cases-behind-100-cpu-usage.png",
        "https://assets.bytebytego.com/diagrams/0021-must-know-website-performance-metrics.png",
        "https://assets.bytebytego.com/diagrams/0372-top-10-k8s-design-patterns.png",
        "https://assets.bytebytego.com/diagrams/0282-top-10-most-popular-open-source-databases.png",
        "https://assets.bytebytego.com/diagrams/0100-eventual-consistency-patterns-you-must-know.png",
        "https://assets.bytebytego.com/diagrams/0049-top-network-security-cheatsheet.png",
        "https://assets.bytebytego.com/diagrams/0097-dbtypes.png",
        "https://assets.bytebytego.com/diagrams/0268-memory-storage.png",
        "https://assets.bytebytego.com/diagrams/0045-memory-types.png",
        "https://assets.bytebytego.com/diagrams/0272-message-queues.png",
        "https://assets.bytebytego.com/diagrams/0404-vpns.png",
        "https://assets.bytebytego.com/diagrams/0123-typical-aws-network-architecture.png",
        "https://assets.bytebytego.com/diagrams/0394-understanding-database-types.png",
        "https://assets.bytebytego.com/diagrams/0400-upi-2.png",
        "https://assets.bytebytego.com/diagrams/0105-id-generator.png",
        "https://assets.bytebytego.com/diagrams/0342-how-does-sso-work.jpeg",
        "https://assets.bytebytego.com/diagrams/0402-vertical-partitioning-vs-horizontal-partitioning.png",
        "https://assets.bytebytego.com/diagrams/0114-sql-query-logical-order.png",
        "https://assets.bytebytego.com/diagrams/0239-isolation-level.png",
        "https://assets.bytebytego.com/diagrams/0022-9-types-of-database-locks.png",
        "https://assets.bytebytego.com/diagrams/0154-cookies-vs-session.png",
        "https://assets.bytebytego.com/diagrams/0269-memory-allocation-paging-vs-segmentation.png",
        "https://assets.bytebytego.com/diagrams/0186-energy-efficient-language.jpg",
        "https://assets.bytebytego.com/diagrams/0280-most-important-aws-services.png",
        "https://assets.bytebytego.com/diagrams/0129-caching-strategy.jpg",
        "https://assets.bytebytego.com/diagrams/0396-typical-microservice-architecture.png",
        "https://assets.bytebytego.com/diagrams/0407-what-does-acid-mean.png",
        "https://assets.bytebytego.com/diagrams/0393-type-a-url-into-your-browser.png",
        "https://assets.bytebytego.com/diagrams/0410-what-happens-when-you-type-google-in-your-browser.png",
        "https://assets.bytebytego.com/diagrams/0169-design-s3.jpg",
        "https://assets.bytebytego.com/diagrams/0043-what-is-a-cookie.png",
        "https://assets.bytebytego.com/diagrams/0411-what-is-a-deadlock.png",
        "https://assets.bytebytego.com/diagrams/0345-stop-loss.jpg",
        "https://assets.bytebytego.com/diagrams/0132-cdn.png",
        "https://assets.bytebytego.com/diagrams/0413-what-is-cloud-native.png",
        "https://assets.bytebytego.com/diagrams/0060-what-is-devsecops.png",
        "https://assets.bytebytego.com/diagrams/0183-elk.jpg",
        "https://assets.bytebytego.com/diagrams/0245-k8s.png",
        "https://assets.bytebytego.com/diagrams/0295-osi-model.jpeg",
        "https://assets.bytebytego.com/diagrams/0329-serverlessdb.jpeg",
        "https://assets.bytebytego.com/diagrams/0031-how-to-learn-sql.png",
        "https://assets.bytebytego.com/diagrams/0304-program-process-thread.png",
        "https://assets.bytebytego.com/diagrams/0416-what-is-web-3.png",
        "https://assets.bytebytego.com/diagrams/0417-what-makes-aws-lambda-so-fast.png",
        "https://assets.bytebytego.com/diagrams/0315-reliable-udp.png",
        "https://assets.bytebytego.com/diagrams/0335-ship-to-prod-tools.png",
        "https://assets.bytebytego.com/diagrams/0333-what-s-the-difference-between-session-based-authentication-and-jwts.png",
        "https://assets.bytebytego.com/diagrams/0250-latency-numbers.jpg",
        "https://assets.bytebytego.com/diagrams/0420-why-cdns-are-so-popular.png",
        "https://assets.bytebytego.com/diagrams/0383-top-6-use-cases-of-distributed-lock.png",
        "https://assets.bytebytego.com/diagrams/0424-why-is-kafka-fast.jpg",
        "https://assets.bytebytego.com/diagrams/0423-why-is-nginx-so-popular.png",
        "https://assets.bytebytego.com/diagrams/0303-postgres.png",
        "https://assets.bytebytego.com/diagrams/0422-why-is-redis-so-fast.png"
    ]
    
    # Ruta donde se guardarán las imágenes (cambia esta ruta según necesites)
    ruta_destino = "/home/debianuser/Downloads/system_design_images"
    
    # Crear el directorio si no existe
    Path(ruta_destino).mkdir(parents=True, exist_ok=True)
    
    # Headers para simular un navegador y evitar bloqueos
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Contador para seguimiento
    descargadas = 0
    errores = 0
    
    print(f"Iniciando descarga de {len(urls)} imágenes...")
    print(f"Directorio de destino: {ruta_destino}")
    print("-" * 50)
    
    for url in urls:
        try:
            # Extraer el nombre del archivo de la URL
            nombre_archivo = unquote(url.split('/')[-1])
            ruta_completa = os.path.join(ruta_destino, nombre_archivo)
            
            # Verificar si el archivo ya existe
            if os.path.exists(ruta_completa):
                print(f"✓ Ya existe: {nombre_archivo}")
                descargadas += 1
                continue
            
            # Descargar la imagen
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()  # Lanza excepción si hay error HTTP
            
            # Guardar la imagen
            with open(ruta_completa, 'wb') as archivo:
                archivo.write(response.content)
            
            print(f"✓ Descargada: {nombre_archivo}")
            descargadas += 1
            
        except requests.exceptions.RequestException as e:
            print(f"✗ Error descargando {url.split('/')[-1]}: {e}")
            errores += 1
        except Exception as e:
            print(f"✗ Error inesperado con {url.split('/')[-1]}: {e}")
            errores += 1
    
    print("-" * 50)
    print(f"Descarga completada:")
    print(f"Imágenes descargadas: {descargadas}")
    print(f"Errores: {errores}")
    print(f"Total procesadas: {descargadas + errores}")

def descargar_con_progreso():
    """Versión alternativa con barra de progreso"""
    from tqdm import tqdm
    import requests
    
    urls = [
        "https://assets.bytebytego.com/diagrams/0147-cloud-evolution.png",
        "https://assets.bytebytego.com/diagrams/0310-qr-code.jpg",
        # ... (todas las URLs)
        "https://assets.bytebytego.com/diagrams/0422-why-is-redis-so-fast.png"
    ]
    
    ruta_destino = "/home/debianuser/Downloads/system_design_images"
    Path(ruta_destino).mkdir(parents=True, exist_ok=True)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
    }
    
    descargadas = 0
    errores = 0
    
    print("Descargando imágenes con barra de progreso...")
    
    for url in tqdm(urls, desc="Progreso"):
        try:
            nombre_archivo = unquote(url.split('/')[-1])
            ruta_completa = os.path.join(ruta_destino, nombre_archivo)
            
            if os.path.exists(ruta_completa):
                descargadas += 1
                continue
            
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            with open(ruta_completa, 'wb') as archivo:
                archivo.write(response.content)
            
            descargadas += 1
            
        except:
            errores += 1
    
    print(f"\nDescargadas: {descargadas}, Errores: {errores}")

if __name__ == "__main__":
    # Instrucciones de uso
    print("Script de descarga de imágenes de System Design")
    print("=" * 50)
    
    # Preguntar al usuario la ruta de destino
    # ruta_predeterminada = "/home/debianuser/Downloads/system_design_images"
    ruta_predeterminada = "/home/debianuser/Documents/proyectos/python/system-design-101/data/images"
    ruta_usuario = input(f"Ruta de destino (presiona Enter para usar '{ruta_predeterminada}'): ").strip()
    
    if not ruta_usuario:
        ruta_usuario = ruta_predeterminada
    
    # Actualizar la ruta de destino
    globals()['ruta_destino'] = ruta_usuario
    
    # Crear el directorio
    Path(ruta_usuario).mkdir(parents=True, exist_ok=True)
    
    # Ejecutar descarga
    try:
        descargar_imagenes()
    except KeyboardInterrupt:
        print("\nDescarga interrumpida por el usuario")