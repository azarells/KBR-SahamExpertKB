import com.hp.hpl.jena.rdf.model.*;
import com.hp.hpl.jena.datatypes.xsd.XSDDatatype;
import java.io.*; import java.util.*;
/** Ubah semua literal xsd:decimal menjadi xsd:double agar builtin aritmatika Jena presisi; simpan sebagai Turtle. */
public class ToDouble {
  public static void main(String[] a) throws Exception {
    Model m = ModelFactory.createDefaultModel(); m.read("file:" + a[0]);
    List<Statement> add = new ArrayList<>(), del = new ArrayList<>();
    for (StmtIterator it = m.listStatements(); it.hasNext();) {
      Statement s = it.next(); RDFNode o = s.getObject();
      if (o.isLiteral() && XSDDatatype.XSDdecimal.getURI().equals(o.asLiteral().getDatatypeURI())) {
        del.add(s); add.add(m.createStatement(s.getSubject(), s.getPredicate(), m.createTypedLiteral(Double.parseDouble(o.asLiteral().getLexicalForm()), XSDDatatype.XSDdouble)));
      }
    }
    m.remove(del); m.add(add);
    m.setNsPrefix("ex", "http://kbr.kelompok9.id/ontologi/SahamExpertKB.owl#");
    try (OutputStream out = new FileOutputStream(a[1])) { m.write(out, "TURTLE"); }
    System.out.println("decimal->double: " + del.size() + " literal; triple=" + m.size());
  }
}
