import { UnrefedKeyword } from "@/lib/models/keyword";
import { Teacher } from "@/lib/models/teacher";
import { TeacherRepository } from "@/lib/repositories/teacher";
import { KeywordUseCase } from "@/lib/usecases/keyword";

export class TeacherUseCase {
  private teacherRepository: TeacherRepository;
  private keywordUseCase: KeywordUseCase;

  constructor() {
    this.teacherRepository = new TeacherRepository();
    this.keywordUseCase = new KeywordUseCase();
  }

  private ranking(keywords: UnrefedKeyword[]): Teacher[] {
    const teachers: Map<string, Teacher> = new Map();
    const scores: Map<string, number> = new Map();

    keywords.forEach((keyword, index) => {
      const weight = 1 / (index + 1);
      keyword.teachers.forEach(teacher => {
        const prevWeight = scores.get(teacher.identifier) || 0;
        teachers.set(teacher.identifier, teacher);
        scores.set(teacher.identifier, prevWeight + weight);
      });
    });

    return Array.from(scores.entries())
      .sort((a, b) => b[1] - a[1])
      .map(entry => entry[0])
      .map(id => teachers.get(id) as Teacher);
  }

  public getById(id: string): Promise<Teacher | undefined> {
    return this.teacherRepository.getById(id);
  }

  public getByIdWithCache(id: string): Promise<Teacher | undefined> {
    return this.teacherRepository.getByIdWithCache(id);
  }

  public getAll(): Promise<Teacher[]> {
    return this.teacherRepository.getAll();
  }

  public getAllWithCache(): Promise<Teacher[]> {
    return this.teacherRepository.getAllWithCache();
  }

  public async findByKeyword(keyword: string): Promise<Teacher[]> {
    const keywords = await this.keywordUseCase.findNearest(keyword);
    const teachers = this.ranking(keywords);
    return teachers;
  }
}
