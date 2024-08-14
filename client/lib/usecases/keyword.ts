import { Keyword, UnrefedKeyword } from "@/lib/models/keyword";
import { Teacher } from "@/lib/models/teacher";
import { KeywordRepository } from "@/lib/repositories/keyword";

export class KeywordUseCase {
  private keywordRepository: KeywordRepository;

  constructor() {
    this.keywordRepository = new KeywordRepository();
  }

  private async unref(keyword: Keyword): Promise<UnrefedKeyword> {
    const snapshots = await Promise.all(keyword.teachers.map(async (ref) => ref.get()));
    const teachers = snapshots.map((snapshot) => snapshot.data()).filter((item): item is Teacher => !!item);

    return {
      keyword: keyword.keyword,
      embedding: keyword.embedding,
      teachers,
    };
  }

  public async findNearest(keyword: string): Promise<UnrefedKeyword[]> {
    const keywords = await this.keywordRepository.findNearest(keyword);
    return Promise.all(keywords.map(this.unref));
  }
}
