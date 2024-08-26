import { trace } from "@opentelemetry/api";

import { Keyword, UnrefedKeyword } from "@/lib/models/keyword";
import { Teacher } from "@/lib/models/teacher";
import { KeywordRepository } from "@/lib/repositories/keyword";

export class KeywordUseCase {
  private keywordRepository: KeywordRepository;

  constructor() {
    this.keywordRepository = new KeywordRepository();
  }

  private async unref(keyword: Keyword): Promise<UnrefedKeyword> {
    return await trace
      .getTracer("GraphTMU")
      .startActiveSpan("KeywordUseCase.unref", async (span) => {
        try {
          const snapshots = await Promise.all(
            keyword.teachers.map(async (ref) => ref.get()),
          );
          const teachers = snapshots
            .map((snapshot) => snapshot.data())
            .filter((item): item is Teacher => !!item);

          return {
            keyword: keyword.keyword,
            embedding: keyword.embedding,
            teachers,
          };
        } finally {
          span.end();
        }
      });
  }

  public async findNearest(keyword: string): Promise<UnrefedKeyword[]> {
    return await trace
      .getTracer("GraphTMU")
      .startActiveSpan("KeywordUseCase.findNearest", async (span) => {
        try {
          const embedding = await this.keywordRepository.getEmbedding(keyword);
          const keywords = await this.keywordRepository.findNearest(embedding);
          return Promise.all(keywords.map(this.unref));
        } finally {
          span.end();
        }
      });
  }
}
